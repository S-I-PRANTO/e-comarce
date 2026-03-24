from django.urls import path,include
# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from product.views import ProductList,CategoryList,ReviewSet,ProductImagesViewset
from order.views import CartViewset,CartItemViewSet,OrderViewset
router=routers.DefaultRouter()
router.register('products',ProductList,basename='product'),
router.register('categorys',CategoryList,basename='category'),
router.register('carts',CartViewset,basename='carts'),
router.register('orders',OrderViewset,basename='orders')



product_router=routers.NestedDefaultRouter(router,'products',lookup='product')
product_router.register('review',ReviewSet,basename='product_review')
product_router.register('images',ProductImagesViewset,basename='images')


cart_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('item',CartItemViewSet,basename='cart_item')

urlpatterns = [
   path('',include(router.urls)),
   path('',include(product_router.urls)),
   path('',include(cart_router.urls)),
   path('auth/', include('djoser.urls')),
   path('auth/', include('djoser.urls.jwt')),

]