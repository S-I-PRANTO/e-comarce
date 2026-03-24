from django.db import models
from django.contrib.auth.models import AbstractUser
from user.manager import CustomUser

class User(AbstractUser):
    username=None
    email=models.EmailField(unique=True)
    address=models.TextField(blank=True,null=True)
    phone_number=models.CharField(max_length=15,blank=True,null=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    objects=CustomUser()
    
    def __str__(self):
        return self.email
    