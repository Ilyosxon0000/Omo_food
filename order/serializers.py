# rest import
from rest_framework import serializers
# local import
from .models import Each_Product,Location,Order

class Each_ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Each_Product
        fields="__all__"

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Location
        fields="__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields="__all__"

class UserRegistrationSerializer(serializers.Serializer):
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    phone=serializers.CharField()

class CheckOutSerializer(serializers.Serializer):
    basket_products=serializers.ListField(child = serializers.IntegerField())
    user=UserRegistrationSerializer()
    location=LocationSerializer()
    address_status=serializers.ChoiceField(choices=Order.ADDRESS_STATUS)

    # class Meta:
    #     model=Order
    #     fields="__all__"
