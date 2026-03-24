from django.contrib.auth.base_user import BaseUserManager

class CustomUser(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("The email fields must be set ")
           
        # email normaliz 
        user=self.normalize_email(email)
        # model set user er email and **extra_fields
        user=self.model(email=email,**extra_fields)
        # user setpassword 
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must be have is_staff = Ture')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_supperuser = True')

        return self.create_user(email,password,**extra_fields)









# class CustomUserManager(BaseUserManager):
#     def create_user(self,email,password=None,**extra_fields):
#         if not email:
#             raise ValueError("This Email field must be set ")
#         email =self.normalize_email(email)
#         user=self.model(email=email,**extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)



#     def create_supperuser(self,email,password=None,**extra_fields):
#         extra_fields.setdefault('is_staff',True)
#         extra_fields.setdefault('is_supperuser',True)
#         if not extra_fields.get('is_staff'):
#             raise ValueError('Superuser must be is_staff=True')
#         if not extra_fields.get('is_superuser'):
#             raise ValueError('Supperuser must be is_supperuser=True')