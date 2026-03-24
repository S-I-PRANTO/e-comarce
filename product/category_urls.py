from django.urls import path
from product.views import CategoryList

urlpatterns = [
    path('',CategoryList.as_view(),name='Category_list'),
    path('<int:pk>/',CategoryList.as_view(),name='specific_category')
]