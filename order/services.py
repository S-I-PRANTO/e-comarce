
from order.models import Cart,Order,OrderItem
from django.db import transaction
from rest_framework.exceptions import ValidationError,PermissionDenied
class OrderClass:
    @staticmethod
    def create(self,user_id,cart_id):
        with transaction.atomic():
            cart=Cart.objects.get(pk=cart_id)
            cartItem=cart.items.select_related('product').all()
            total_price=[item.product.price * item.quantity for item in cartItem]

            order=Order.objects.create(user_id=user_id,total_price=total_price)

            orderItem=[
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                    total_price=item.product.price * item.quantity
                ) for item in cartItem
            ]

            Order.objects.bulk_create(orderItem)

            cart.delete()


    @staticmethod
    def Canceled(user,order):
        if user.is_staff:
            order.status=Order.CANCELED
            order.save()
            return order
        
        if order.user != user:
            raise PermissionDenied("You can only cancel your own order.")
        
        if order.status == Order.DELIVERED:
            raise ValidationError("You can not cancel an order," \
            "Because this items is already processing into order ")
        
        order.status=Order.CANCELED
        order.save()
        return order