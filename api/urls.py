from django.urls import path, include
from api import views


urlpatterns = [

    #Widoki do obsługi zdarzeń związanych z produktami
    path('api/products/',views.ProductList.as_view()), #lista produktów
    path('api/products/create',views.ProductCreate.as_view()), #tworzenie produktu
    path('api/products/<int:pk>/',views.ProductDetail.as_view()), #szczegóły produktu
    path('api/products/<int:pk>/edit/',views.ProductEdit.as_view()), #edycja produktu(modyfikacja,usuwanie)

    #Widoki do obsługi zdarzeń związanych z zamówieniami
    path('api/products_order/',views.ProductOrderList.as_view()), #lista zamówień
    path('api/products_order/create/',views.ProductOrderCreate.as_view()), #tworzenie nowego zamówienia

    #Widoki do obsługi zdarzeń związanych z kategoriami produktów
    path('api/products_category/create',views.ProductCategoryCreate.as_view()), #tworzenie nowej kategorii
    path('api/products_category/<int:pk>/',views.ProductCategoryDetails.as_view(),name='category-detail'), #szczegóły kategorii

    #Widok z najlepiej sprzedającymi się produktami
    path('api/products/best/',views.BestSellingProducts.as_view()),

    #Widoki do obsługi zdarzeń związanych z użytkownikami
    path('api/users/',views.UserList.as_view()),
    path('api/users/create/',views.UserCreate.as_view()),

    #Widoki bazowe Django Rest Framework
    path('api-auth/',include('rest_framework.urls')),
]