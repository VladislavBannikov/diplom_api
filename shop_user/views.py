from django.shortcuts import render
from rest_framework import viewsets, permissions, authentication, throttling, status, views, generics, \
    exceptions, validators
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from django.contrib.auth.password_validation import validate_password

from shop_user.models import User, ConfirmEmailToken, Contact
from shop_user.serializers import UserSerializer, ContactSerializer


class Account(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'], url_name='detail', permission_classes=(permissions.IsAuthenticated,))
    def details(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], url_name='confirm', )
    def confirm(self, request, *args, **kwargs):
        # проверяем обязательные аргументы
        if {'email', 'token'}.issubset(request.data):
            token = ConfirmEmailToken.objects.filter(user__email=request.data['email'],
                                                     key=request.data['token']).first()
            if token:
                token.user.is_active = True
                token.user.save()
                token.delete()
                return JsonResponse({'Status': True})
            else:
                return JsonResponse({'Status': False, 'Errors': 'Неправильно указан токен или email'})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    # TODO: роутер при создание URL для этого действия генерирует <URLPattern '^account/$' [name='user-list']>,
    # что не соответствует назначению - создание пользователя. Лучше если будет name=user-create.
    # можно ли переопределить?
    # TODO: OpenAPI auto_schema generates schema without password field. Create custom auto_schema
    def create(self, request, *args, **kwargs):
        if not {'first_name', 'last_name', 'email', 'password', 'company', 'position'}.issubset(request.data):
            raise exceptions.ValidationError(detail='Не указаны все необходимые аргументы', code=None)
        try:
            validate_password(request.data['password'])
        except Exception as password_error:
            raise exceptions.ValidationError(detail=password_error, code=None)
        return viewsets.mixins.CreateModelMixin.create(self, request, *args, **kwargs)

    # override from viewsets.mixins.CreateModelMixin
    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(self.request.data['password'])
        user.save()
        # TODO: check if it still works
        ##calary task
        # print('task')
        # task = new_user_registered_task.delay(user.id)
        # print(f"id={task.id}, state={task.state}, status={task.status}")
        # print('signal')
        # new_user_registered.send(sender=self.__class__, user_id=user.id)

    @action(detail=False, methods=['POST'], url_name='edit', permission_classes=(permissions.IsAuthenticated,))
    def edit(self, request, *args, **kwargs):
        # проверяем обязательные аргументы
        if 'password' in request.data:
            errors = {}
            # проверяем пароль на сложность
            try:
                validate_password(request.data['password'])
            except Exception as password_error:
                error_array = []
                # noinspection PyTypeChecker
                for item in password_error:
                    error_array.append(item)
                return JsonResponse({'Status': False, 'Errors': {'password': error_array}})
            else:
                request.user.set_password(request.data['password'])
        # проверяем остальные данные
        user_serializer = UserSerializer(request.user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse({'Status': True})
        else:
            return JsonResponse({'Status': False, 'Errors': user_serializer.errors})


class ContactViewSet(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin, viewsets.mixins.ListModelMixin,
                     viewsets.mixins.UpdateModelMixin, viewsets.mixins.DestroyModelMixin):
    serializer_class = ContactSerializer

    def get_queryset(self):
        user = self.request.user
        return Contact.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        request.data.update({"user": request.user.id})
        return super().create(request, *args, **kwargs)


class CustomObtainAuthToken(ObtainAuthToken):
    throttle_classes = (throttling.AnonRateThrottle,)
