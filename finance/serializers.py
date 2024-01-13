from rest_framework import serializers
from finance.models import Product,Order

class FinanceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"

class FinanceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields="__all__"
