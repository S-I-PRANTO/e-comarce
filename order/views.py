from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
from rest_framework.decorators import action
from order.serializers import CartSerializer,CartItemSerializer,AddToItemSerializer,UpdateCartSerializer,OrderSerializer,CreateOrderSerializer,OrderUpdateSerializer,EmptySerializer
from order.services import OrderClass
from order.models import Cart,CartItem,Order
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response


class CartViewset(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
   
    serializer_class=CartSerializer
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if getattr(self,'swagger_fake_view',False):
            return Cart.objects.none()
        return Cart.objects.prefetch_related('items').filter(user=self.request.user)
    

class CartItemViewSet(ModelViewSet):

    http_method_names=['get','post','patch','delete']
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddToItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id':self.kwargs.get('cart_pk')}

    def get_queryset(self):
        cart_pk = self.kwargs.get('cart_pk')
        return CartItem.objects.filter(cart_id=cart_pk).select_related('product')


class OrderViewset(ModelViewSet):

    http_method_names=['get','post','patch','delete','head','options']
    @action(detail=True,methods=['post'])
    def cancel(self,request,pk=None):
        order=self.get_object()
        OrderClass.Canceled(user=request.user,order=order)
        return Response({'status':'Order is canceled'})
    

    @action(detail=True,methods=['patch'])
    def update_status(self,request,pk=None):
        order=self.get_object()
        updateSerializer=OrderUpdateSerializer(order,data=request.data,partial=True)
        updateSerializer.is_valid(raise_exception=True)
        updateSerializer.save()
        return Response({'status': f"Order status update to {request.data['status']}"})

    def get_permissions(self):
        if self.action in ['update_status','destroy']:
            return[IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action =='cancel':
            return EmptySerializer
        elif self.action == 'create':
            return CreateOrderSerializer
        elif self.action == 'update_status':
            return OrderUpdateSerializer
        return OrderSerializer

    def get_serializer_context(self):
         if getattr(self,'swagger_fake_view',False):
             return super().get_serializer_context()
         return{'user_id':self.request.user.id}

    def get_queryset(self):
        if getattr(self,'swagger_fake_view',False):
            return Order.objects.none()

        if self.request.user.is_staff:
            return Order.objects.prefetch_related('orderItem').all()
        return Order.objects.filter(user=self.request.user).prefetch_related('orderItem')
    

















# class OrderItemViewSet(ModelViewSet):
#     permission_classes=[IsAuthenticated]



#     def get_serializer_class(self):
#         if self.request.method =='POST':
#             return CreateOrderserializer
#         return OrderSerializer
    

#     def get_queryset(self):
#         if self.request.user.is_staff:
#             return Order.objects.prefetch_related('orderItem').all()
#         return Order.objects.filter(user=self.request.user).prefetch_related('orderItem')
    









# class CartItemViewSet(ModelViewSet):
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return AddCartItemSerializer
#         return CartItemSerializer
#     def get_serializer_context(self):
#         return {'cart_id':self.kwargs.get('cart_id')}

#     def get_queryset(self):
#         return CartItem.objects.filter(cart_id=self.kwargs.get('cart_pk'))
