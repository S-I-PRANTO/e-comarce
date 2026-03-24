from django.urls import path,include
from product.views import ProductList

urlpatterns = [
    path('',ProductList.as_view,name='product_list'),
    path('<int:pk>/',ProductList.as_view,name='specific_product')
]