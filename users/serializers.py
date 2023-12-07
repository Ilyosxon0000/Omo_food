# rest framework
from rest_framework import serializers
from rest_framework.utils import model_meta
# django
from django.contrib.auth import get_user_model
# local import
from .models import Basket

import traceback

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
    