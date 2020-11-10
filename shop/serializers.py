from django.db.models import QuerySet, F
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from shop.models import User, Category, Shop, ProductInfo, Product, ProductParameter, OrderItem, Order, Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'user', 'phone')
        read_only_fields = ('id',)
        extra_kwargs = {
            'user': {'write_only': True}
        }


class UserSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'company', 'position', 'contacts')
        read_only_fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'state',)
        read_only_fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('name', 'category',)


class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = serializers.StringRelatedField()

    class Meta:
        model = ProductParameter
        fields = ('parameter', 'value',)


class ProductInfoSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_parameters = ProductParameterSerializer(read_only=True, many=True)

    class Meta:
        model = ProductInfo
        fields = ('id', 'model', 'product', 'shop', 'quantity', 'price', 'price_rrc', 'product_parameters',)
        read_only_fields = ('id',)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product_info', 'quantity', 'order',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'order': {'write_only': True}
        }


class OrderItemCreateSerializer(OrderItemSerializer):
    product_info = ProductInfoSerializer(read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    ordered_items = OrderItemCreateSerializer(read_only=True, many=True)

    total_sum = serializers.IntegerField()
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'ordered_items', 'state', 'dt', 'total_sum', 'contact',)
        read_only_fields = ('id',)


class OrderSerializerViewSet(serializers.ModelSerializer):
    ordered_items = OrderItemCreateSerializer(read_only=True, many=True)
    contact = ContactSerializer()

    # explicit definition to avoid readOnly flag
    contact_id = serializers.IntegerField()

    # TODO: how to hide contact_id from GET request but use it in PUT and POST?
    class Meta:
        model = Order
        fields = ('id', 'state', 'dt', 'ordered_items', 'contact_id', 'contact', 'total_sum2')
        read_only_fields = ('id',)

        # validators = UniqueTogetherValidator

    def validate_state(self, value):
        if self.instance.state != 'basket':
            raise serializers.ValidationError("Order already has been placed")
        return value

    def validate(self, data):
        new_contact = Contact.objects.get(id=data['contact_id'])
        if new_contact.user_id != self.instance.user_id:
            raise serializers.ValidationError("Order contact should belong to the user who created the order")
        return data

    # def __new__(cls, *args, **kwargs):
    #     if args and isinstance(args[0], QuerySet):
    #         queryset = cls._build_queryset(args[0])

    #         args = (queryset,) + args[1:]
    #     return super().__new__(cls, *args, **kwargs)
    #
    # @classmethod
    # def _build_queryset(cls, queryset):
    #     return queryset.annotate(
    #         total_sum=
    #         # sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))
    #     )


class SingleProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    product_infos = ProductInfoSerializer(read_only=True, many=True)
    product_parameters = ProductParameterSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ('name', 'category', 'product_infos', 'product_parameters')
