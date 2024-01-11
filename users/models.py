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

class Basket(models.Model):
    user=models.ForeignKey(get_user_model(),related_name="basket_products",on_delete=models.CASCADE)
    product=models.ForeignKey(Product,related_name="baskets",on_delete=models.CASCADE)
    amount=models.IntegerField(default=1)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    
    def get_total_price(self)->dict:
        product=self.product
        if self.amount>product.amount:
                self.amount=product.amount
                self.save()
        discount=product.check_discount()
        data={
            "price":self.product.price*self.amount
        }
        if discount:
            data["discount_price"]=discount['product_discount_price']*self.amount
        return data

    @classmethod
    def get_total_price_all(cls,user)->dict:
        basket_products=cls.objects.filter(user=user,is_active=True)
        data={
            "price":0,
            "discount_price":0
        }
        for item in basket_products:
            item_total_price=item.get_total_price()
            discount_price=item_total_price.get("discount_price",0)
            data['price']+=item_total_price['price']
            data['discount_price']+=discount_price
            if discount_price==0 and data["discount_price"]:
                data["discount_price"]+=item_total_price['price']
        # percentage=data['price']/100
        # benefit=data['price']-data["discount_price"]
        # benefit_percentage=benefit/percentage
        return data

