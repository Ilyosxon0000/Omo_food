# rest framework
from rest_framework import serializers
# django
from django.contrib.auth import get_user_model
# local import
from .models import Basket
from products.serializers import ProductSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
        ]
        # extra_kwargs = {"password": {"write_only": True}}

class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model=Basket
        fields="__all__"

    def __init__(self, *args, **kwargs):
        super(BasketSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request", None)
        if request and request.method == "GET":
            products=request.GET.get("products",None)=='true'
            if products:
                self.fields["product"] = ProductSerializer(context=self.context)
                # self.fields["total_price"] = serializers.FloatField(source='get_total_price')
            total_price=request.GET.get("total_price",None)=='true'
            if total_price:
                self.fields["total_price"] = serializers.DictField(source='get_total_price')
