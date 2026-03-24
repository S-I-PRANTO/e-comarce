from django.db import models
from uuid import uuid4
from user.models import User
from product.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator

class Cart(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid4,editable=False)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='cart')
    created_at=models.DateTimeField(auto_now_add=True)

    class Mata:
        unique_together=[['cart','product']]

    def __str__(self):
        return f"Cart of {self.user.email}"
    

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(validators=[MinValueValidator(1)])


    def __str__(self):
        return f"{self.quantity} X {self.product.name} by   ___  {self.cart.user.email}"
    
class Order(models.Model):
    NOT_PAID='Not_Paid'
    READY_TO_SHIP='Ready_To_Ship'
    PENDING='Pending'
    SHIPPED='Shipped'
    DELIVERED='Delivered'
    CANCELED='Canceled'
    STATUS_CHOICES=[
        (NOT_PAID,'Not_Paid'),
        (READY_TO_SHIP,'Ready_To_Ship'),
        (PENDING,'Pending'),
        (SHIPPED,'Shipped'),
        (DELIVERED,'Delivered'),
        (CANCELED,'Canceled')
    ]
    id=models.UUIDField(primary_key=True,default=uuid4,editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default=PENDING)
    total_price=models.DecimalField(max_digits=10,decimal_places=2)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by --- {self.user.email} --- and {self.status}"
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='orderItem')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    def __str__(self):
        return f"Id: {self.order.id}   ____    Quantity: {self.quantity}  ____  Name: {self.product.name}    ____  Customer: {self.order.user.email} "
    