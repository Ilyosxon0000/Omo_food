from django.db import models
from django.contrib.auth import get_user_model
# local import
from products.models import Product 

# Create your models here.

class Each_Product(models.Model):
    product=models.ForeignKey(Product,related_name="each_product",on_delete=models.PROTECT)
    amount=models.IntegerField(default=1)
    total_price=models.FloatField(default=0)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)

class Order(models.Model):
    user=models.ForeignKey(get_user_model(),related_name="orders",on_delete=models.PROTECT)
    each_products=models.ForeignKey(Each_Product,related_name="orders",on_delete=models.PROTECT)
    total_price=models.FloatField(default=0)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)