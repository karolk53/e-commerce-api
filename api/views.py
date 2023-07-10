from django.core.mail import send_mail
from django.db.models import Sum
from rest_framework import filters
from .serializers import UserSerializer,ProductSerializer, ProductCategorySerializer, ProductOrderSerializer, ProductOrderListSerializer, ProductAllSerializer
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSeller,IsCustomer
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from api import models

User = get_user_model()


#USER SECTION
class UserCreate(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


#PRODUCT CATEGORY SECTION
class ProductCategoryCreate(CreateAPIView):
    queryset = models.ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class ProductCategoryDetails(RetrieveAPIView):
    queryset = models.ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


#PRODUCT SECTION
class ProductCreate(CreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated,IsSeller]


class ProductList(ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductAllSerializer
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ['name', 'description','category__name','price']
    filterset_fields = ['name', 'description', 'category__name', 'price']
    ordering_fields = ['name','category__name','price']


class ProductDetail(RetrieveAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductAllSerializer


class ProductEdit(RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSeller]


#ORDER SECTION
class ProductOrderCreate(CreateAPIView):
    queryset = models.ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer
    permission_classes = [IsAuthenticated,IsCustomer]

    def perform_create(self, serializer):

        order = serializer.save()

        subject = "Potwierdzenie"
        contents = f"Zamównie nr.{order.id} zostało poprawnie złożone"
        email = self.request.user.email

        send_mail(
            subject,
            contents,
            'company_email@example.com',
            [email],
            fail_silently=False,
        )


class ProductOrderList(ListAPIView):
    queryset = models.ProductOrder.objects.all()
    serializer_class = ProductOrderListSerializer


#BEST SELLING PRODUCTS
class BestSellingProducts(ListAPIView):
    serializer_class = ProductAllSerializer

    def get_queryset(self):
        queryset = models.Product.objects.annotate(num_orders=Sum('orderitem__quantity')).order_by('-num_orders')
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        num_products = self.request.query_params.get('num_products', 2)

        if date_from and date_to:
            queryset = queryset.filter(orderitem__order__order_date__range=[date_from, date_to])

        return queryset[:num_products]