from rest_framework import serializers
from .models import Each_Product,Order

class Each_ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Each_Product
        fields="__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields="__all__"
