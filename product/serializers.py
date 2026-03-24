from rest_framework import serializers
from decimal import Decimal
from product.models import Categroy ,Product,Review,ProductImages
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Categroy
        fields=['id','name','description','product_count']

    product_count=serializers.IntegerField()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields= ['id','name','description','price','stock','categroy','price_with_tax']

    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
    
    def calculate_tax(self,product):
        return round(product.price * Decimal(1.1),2)
    

    def validate_price(self,price):
        if price <0:
            raise serializers.ValidationError('Price could not be negative ')
        return price

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImages
        fields=['id','images']





class UserShowSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField(method_name='get_current_user')
    class Meta:
        model=get_user_model()
        fields=['id','name']

    def get_current_user(self,obj):
        return obj.get_full_name()
    
    
class ReviewSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField(method_name='get_data')
    class Meta:
        model=Review
        fields=['id','user','rating','comment']
        read_only_fields=['user']
        
    def get_data(self,obj):
        return UserShowSerializer(obj.user).data
    
    
    def create(self,validated_data):
        product_id=self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)

