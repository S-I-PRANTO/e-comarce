from rest_framework import serializers
from order.models import Cart,CartItem,Order,OrderItem
from product.serializers import ProductSerializer
from product.models import Product
from order.services import OrderClass
class SpecificProductObject(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields= ['id','name','price','stock','categroy']


class EmptySerializer(serializers.Serializer):
    pass

class CartItemSerializer(serializers.ModelSerializer):
    
    product=SpecificProductObject()
    total_item_price=serializers.SerializerMethodField(method_name='total_price_of_product')
    class Meta:
        model=CartItem
        fields=['id','product','quantity','total_item_price']

    def total_price_of_product(self,cart_item:CartItem):
        return cart_item.quantity * cart_item.product.price

class AddToItemSerializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField()

    class Meta:
        model=CartItem
        fields=['id','product_id','quantity']

    def save(self, **kwargs):
        cart_id=self.context['cart_id']
        product_id=self.validated_data['product_id']
        quantity=self.validated_data['quantity']

        try:
            cart_item=CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            cart_item.quantity+=quantity
            self.instance=cart_item.save()
        
        except CartItem.DoesNotExist:
            self.instance=CartItem.objects.create(cart_id=cart_id,**self.validated_data)

        return self.instance


    def validate_product_id(self,value):
        
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"Product with{value} id doesn't extist")
        
        return value

class UpdateCartSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['quantity']



class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True,read_only=True)
    cart_total_price=serializers.SerializerMethodField(method_name='total_price')

    class Meta:
        model=Cart
        fields=['id','user','items','cart_total_price']
        read_only_fields=['user']

    def total_price(self,cart_price:Cart):
        return sum([item.product.price * item.quantity for item in cart_price.items.all()])

class CreateOrderSerializer(serializers.Serializer):
    cart_id=serializers.UUIDField()

    def validate_cart_id(self,cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError("This cart id {cart_id} is not exists!")
        if not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError("The cart is empty ")
        return cart_id
    
    def create(self, validated_data):
        user_id=self.context['user_id']
        cart_id=validated_data['cart_id']
       
        try:
            order=OrderClass.create(user_id=user_id,cart_id=cart_id)
            return order
        except ValueError as e:
            raise serializers.ValidationError(str(e))
    
    def to_representation(self, instance):
        return OrderSerializer(instance).data

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['status']

    

class OrderItemSerializer(serializers.ModelSerializer):
    product=SpecificProductObject()
    class Meta:
        model=OrderItem
        fields=['id','product','quantity','price','total_price']



class OrderSerializer(serializers.ModelSerializer):
    orderItem=OrderItemSerializer(many=True)
    class Meta:
        model=Order
        fields=['id','user','status','orderItem','total_price','created_at']













# class OrderItemSerializer(serializers.ModelSerializer):
#     product=SpecificProductObject()
#     class Meta:
#         model=OrderItem
#         fields=['id','product','quantity','price','total_price']



# class CreateOrderserializer(serializers.Serializer):
#     cart_id=serializers.UUIDField()

#     def validate_cart_id(self,cart_id):
#         if not Cart.objects.filter(pk=cart_id).exists():
#             raise serializers.ValidationError("No cart found with this {cart_id}")
    
#         if not CartItem.objects.filter(cart_id=cart_id).exists():
#             raise serializers.ValidationError("Cart is empty")
        
#         return cart_id
        




# class OrderSerializer(serializers.ModelSerializer):
#     orderItem=OrderItemSerializer(many=True)
#     class Meta:
#         model=Order
#         fields=['id','user','status','total_price','created_at','orderItem']