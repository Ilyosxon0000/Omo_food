from typing import Any
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
    DELIVERY_STATUS=(
        ("QABUL QILINDI","QABUL QILINDI"),
        ("YETKAZILMOQDA","YETKAZILMOQDA"),
        ("YETKAZILDI","YETKAZILDI")
    )
    PAYMENT_METHODS=(
        ("NAQD","NAQD"),
        ("TO'LOV TIZIMI","TO'LOV TIZIMI")
    )
    user=models.ForeignKey(get_user_model(),related_name="orders",on_delete=models.PROTECT)
    each_products=models.ForeignKey(Each_Product,related_name="orders",on_delete=models.PROTECT)
    total_price=models.FloatField(default=0)
    delivery_status=models.CharField(max_length=50,default="QABUL QILINDI",choices=DELIVERY_STATUS)
    payment_method=models.CharField(max_length=50,default="NAQD",choices=PAYMENT_METHODS)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)