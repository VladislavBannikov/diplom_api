from copy import copy
from pprint import pprint

import rest_framework
from celery import current_app
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import IntegrityError
from django.db.models import Q, Sum, F
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from django.shortcuts import render
from json import loads as load_json

from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import APIException

from .permissions import OrderPermission, OnlyBuyers

from rest_framework import viewsets, permissions, authentication, throttling, status, views, generics
from yaml import load as load_yaml, Loader

# Create your views here.
from requests import get
from rest_framework.views import APIView
from rest_framework.response import Response

from shop.models import Shop, Category, Product, ProductInfo, ProductParameter, Parameter, Order, OrderItem
from shop.serializers import ProductInfoSerializer, SingleProductSerializer, \
    OrderItemSerializer, OrderSerializer, OrderSerializerViewSetWrite, OrderSerializerViewSetRead, \
    BasketSerializer
from shop.tasks import new_order_task, new_user_registered_task


class InitData(APIView):
    """
    simulate data upload from shop source
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        with open('data/shop1.yaml', 'r', encoding='utf8') as f:
            stream = f.read()
            resp = StreamingHttpResponse(streaming_content=stream)
            return resp
        return JsonResponse({'Status': False, 'Error': 'Ошибка загрузки файла'}, status=403)


class PartnerUpdate(APIView):
    """
    Класс для обновления прайса от поставщика
    """

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if request.user.type != 'shop':
            return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        url = request.data.get('url')
        if url:
            validate_url = URLValidator()
            try:
                validate_url(url)
            except ValidationError as e:
                return JsonResponse({'Status': False, 'Error': str(e)})
            else:
                stream = get(url).content

                data = load_yaml(stream, Loader=Loader)

                shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=request.user.id)
                for category in data['categories']:
                    category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
                    category_object.shops.add(shop.id)
                    category_object.save()
                ProductInfo.objects.filter(shop_id=shop.id).delete()
                for item in data['goods']:
                    product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

                    product_info = ProductInfo.objects.create(product_id=product.id,
                                                              external_id=item['id'],
                                                              model=item['model'],
                                                              price=item['price'],
                                                              price_rrc=item['price_rrc'],
                                                              quantity=item['quantity'],
                                                              shop_id=shop.id)
                    for name, value in item['parameters'].items():
                        parameter_object, _ = Parameter.objects.get_or_create(name=name)
                        ProductParameter.objects.create(product_info_id=product_info.id,
                                                        parameter_id=parameter_object.id,
                                                        value=value)

                return JsonResponse({'Status': True})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class ProductInfoView(APIView):
    """
    Класс для поиска товаров
    """

    def get(self, request, *args, **kwargs):

        query = Q(shop__state=True)
        shop_id = request.query_params.get('shop_id')
        category_id = request.query_params.get('category_id')

        if shop_id:
            query = query & Q(shop_id=shop_id)

        if category_id:
            query = query & Q(product__category_id=category_id)

        # фильтруем и отбрасываем дуликаты
        queryset = ProductInfo.objects.filter(
            query).select_related(
            'shop', 'product__category').prefetch_related(
            'product_parameters__parameter').distinct()
        print(queryset)
        serializer = ProductInfoSerializer(queryset, many=True)

        return Response(serializer.data)


class BasketListView(generics.ListAPIView):
    """
    GET (list basket)
    """
    permission_classes = (OnlyBuyers,)
    serializer_class = BasketSerializer

    def get_queryset(self):
        return Order.objects.filter(user_id=self.request.user.id, state='basket')


class BasketViewSet(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin, viewsets.mixins.DestroyModelMixin,
                    viewsets.mixins.UpdateModelMixin):
    """
    PATCH (update quantity), DELETE, POST (create new item)
    """
    permission_classes = (OnlyBuyers,)

    def get_queryset(self):
        basket_items = OrderItem.objects.filter(order=self.get_basket_id())
        return basket_items

    serializer_class = OrderItemSerializer

    def get_basket_id(self):
        basket, _ = Order.objects.get_or_create(user_id=self.request.user.id, state='basket')
        return basket.id

    # TODO: implement a ListSerializer for multiple orderItem creation and update
    # TODO: constraint exception of DB
    # ==django.db.utils.IntegrityError: UNIQUE    constraint    failed: shop_orderitem.order_id, shop_orderitem.product_info_id==
    # где лучше всего отлавливать подобную ситуацию? Переопределить create или perform_create?

    # request data example - {"quantity":77,"product_info":3}. POST
    def create(self, request, *args, **kwargs):
        # TODO: for future multiple object creation
        # for r in request.data:
        #     r.update({"order": self.get_basket_id()})
        request.data.update({"order": self.get_basket_id()})
        return super().create(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     try:
    #         return super().create(self, request, *args, **kwargs)
    #     except IntegrityError as ex:
    #         print("---", ex)
    #         return Response('failed')


class OrderBuyerViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    """
    create (POST) - place order. Contact_id  is required
    list (GET) - get buyer's orders
    """
    permission_classes = (OnlyBuyers,)
    queryset = Order.objects.all().exclude(state='basket')
    serializer_class = OrderSerializerViewSetRead

    def get_basket(self):
        basket, _ = Order.objects.get_or_create(user_id=self.request.user.id, state='basket')
        return basket

    def create(self, request):
        """
        Place an order (goods from a basket)
        POST with contact_id parameter
        """
        basket = self.get_basket()
        self.request.data.update({"state": "new"})
        serializer = OrderSerializerViewSetWrite(instance=basket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)



class PartnerOrders(APIView):
    """
    Класс для получения заказов поставщиками
    """

    def get(self, request, *args, **kwargs):
        if request.user.type != 'shop':
            return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        order = Order.objects.filter(
            ordered_items__product_info__shop__user_id=request.user.id).exclude(state='basket').prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter').select_related('contact').annotate(
            total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()

        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)


class SingleProductInfoView(APIView):
    """"
    Карточка товара
    get product info by product_id
    """

    def get(self, request, *args, **kwargs):
        product_id = request.query_params.get('product_id')

        if product_id:
            query = Q(id=product_id)
            queryset = Product.objects.filter(query)
            serializer = SingleProductSerializer(queryset, many=True)
            return Response(serializer.data)

        else:
            return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class CeleryTaskView(APIView):
    def get(self, request):
        task_id = request.query_params.get('task_id')
        task = current_app.AsyncResult(task_id)
        response_data = {'task_status': task.status, 'task_id': task.id}

        if task.status == 'SUCCESS':
            response_data['results'] = task.get()

        return JsonResponse(response_data)
