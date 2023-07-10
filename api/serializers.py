from datetime import date, timedelta
from api.models import Product,ProductOrder,ProductCategory,OrderItem
from rest_framework import serializers
from django.contrib.auth import get_user_model
from PIL import Image

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):

    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password','is_customer','is_seller']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            is_customer=validated_data['is_customer'],
            is_seller=validated_data['is_seller']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ['id','name']


class ProductSerializer(serializers.ModelSerializer):

    category = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all())
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:

        model = Product
        fields = ['id','name','description','price','category','image']

    def create(self, validated_data):
        instance = Product.objects.create(**validated_data)

        instance.save()
        return instance


class ProductAllSerializer(serializers.ModelSerializer):

    category = ProductCategorySerializer()

    class Meta:

        model = Product
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):

    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id','product','quantity']


class ProductOrderSerializer(serializers.ModelSerializer):

    products = OrderItemSerializer(many=True)

    class Meta:
        model = ProductOrder
        fields = ['adres','products']

    def create(self, validated_data):
        items = validated_data.pop('products')

        client_id = self.context['request'].user.id

        payment_due_date = date.today() + timedelta(days=5)
        instance = ProductOrder.objects.create(**validated_data,payment_date=payment_due_date,summary_price=300,client_id=client_id)

        summ_price = 0

        for item in items:
            orderitem = OrderItem.objects.create(**item)
            instance.products.add(orderitem)
            orderitem.save()
            instance.save()

            summ_price += orderitem.quantity * orderitem.product.price

        instance.summary_price = summ_price
        instance.save()

        return instance


class ProductOrderListSerializer(serializers.ModelSerializer):

    products = OrderItemSerializer(many=True)
    client = UserSerializer()

    class Meta:
        model = ProductOrder
        fields = '__all__'