# django import
from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
# local import
from products.models import Product
class CustomUserManager(UserManager):
    def create_fake_user(self):
        # Generate a unique username
        username = get_random_string(length=10)
        # Generate a strong password (you can customize the logic for a strong password)
        password = get_random_string(length=12)
        # Create a new user with the generated username and password
        user = self.create_user(username=username, password=password)
        return user

class CustomUser(AbstractUser):
    phone=models.CharField(max_length=13,default="+998901234567")
    objects = CustomUserManager()
    
    def save(self,*args,**kwargs):
        if self.phone[1:].isdigit():
            return super().save(*args,**kwargs)
        return ValidationError("Telefon Raqam noto'g'ri kiritilgan!")
    
    @property
    def get_order(self):
        orders=self.orders.all()
        if orders:
            return orders
        return False

class Location(models.Model):
    user=models.OneToOneField(get_user_model(),related_name="location",on_delete=models.CASCADE)
    address=models.TextField(blank=True,null=True)
    longitude=models.CharField(max_length=200,blank=True,null=True)
    latitude=models.CharField(max_length=200,blank=True,null=True)

class Basket(models.Model):
    user=models.ForeignKey(get_user_model(),related_name="basket_products",on_delete=models.CASCADE)
    product=models.ForeignKey(Product,related_name="baskets",on_delete=models.CASCADE)
    amount=models.IntegerField(default=1)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)

    