from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.

class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)
    is_verified=models.BooleanField(default=False)
    address_line1=models.CharField(null=True,blank=True, max_length=200)
    address_line2=models.CharField(null=True,blank=True, max_length=200)
    city=models.CharField(null=True,blank=True, max_length=200)
    state=models.CharField(null=True,blank=True, max_length=200)
    zip_code=models.CharField(null=True,blank=True, max_length=200)
    country=models.CharField(null=True,blank=True, max_length=200)
    mobile=models.CharField(null=True,blank=True, max_length=200)

    profile_picture=models.ImageField(upload_to='user_profile',null=True,blank=True)
    username = None
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def full_name(self):   
        return f"{self.first_name} {self.last_name}"