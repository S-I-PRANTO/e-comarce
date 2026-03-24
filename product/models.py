from django.db import models
from uuid import uuid4
from django.conf import settings
from django.core.validators import MaxValueValidator,MinValueValidator
from product.validation import validate_file
class Categroy(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):

    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField()
    categroy=models.ForeignKey(Categroy,on_delete=models.CASCADE,related_name='products')
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)


    class Meta:
        ordering=['-id',]
    def __str__(self):
        return self.name
    
class ProductImages(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    images=models.ImageField(upload_to='products/images',validators=[validate_file])
class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.TextField()
    create_date=models.DateField(auto_now_add=True)
    update_date=models.DateField(auto_now=True)


    def __str__(self):
        return "f Rating by {self.user.fast_name} this {self.product.title} "
    