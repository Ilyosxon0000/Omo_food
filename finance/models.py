from django.db import models

# Create your models here.

class Product(models.Model):
    title=models.CharField(max_length=255)

class Order(models.Model):
    product=models.ForeignKey(Product,related_name="orders",on_delete=models.PROTECT)
    price=models.FloatField(default=0)
    amount=models.IntegerField(default=0)
    comment=models.TextField(blank=True,null=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return self.amount*self.price
    