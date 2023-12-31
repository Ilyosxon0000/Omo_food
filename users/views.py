from datetime import datetime,timedelta
# rest_framework import
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
# django import
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
# simple jwt
from rest_framework_simplejwt.tokens import RefreshToken
# local app import
from .serializers import CustomUserSerializer,BasketSerializer
from .models import Basket
from products.models import Product
from conf.views import AuthModelViewSet

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False,methods=['GET'])
    def get_token(self,request,*args,**kwargs):
        fake_user=get_user_model().objects.create_fake_user()
        refresh = RefreshToken.for_user(fake_user)
        access_token = str(refresh.access_token)
        response_data = {
            'access_token': access_token,
        }
        return Response(response_data,status=status.HTTP_200_OK)#TODO HttpOnly technology tutorial

    @action(detail=False, methods=['post'])
    def check_token(self, request):
        return Response({'detail': 'Access token is valid'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def auto_delete_user(self, request, *args, **kwargs):
        # Get the current date and time
        current_date = timezone.now()
        # Calculate the date one month ago
        one_month_ago = current_date - timezone.timedelta(days=30)
        # Filter users based on last_login
        queryset = self.filter_queryset(self.get_queryset())
        inactive_users = queryset.filter(Q(last_login__lt=one_month_ago) | Q(last_login__isnull=True) & Q(get_orders=False))

        inactive_users.delete()
        return Response({"message": "Inactive users deleted successfully."}, status=status.HTTP_200_OK)

class BasketViewSet(AuthModelViewSet):
    queryset=Basket.objects.all()
    serializer_class=BasketSerializer

    def get_queryset(self):
        if self.get_user().is_superuser:
            return super().get_queryset()
        return self.queryset.filter(user=self.get_user())

    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        instance=Basket.objects.get_or_create(user=self.get_user(),product=Product.objects.get(id=self.data['product']))[0]
        instance.amount=self.data.get("amount",instance.amount)
        instance.save()

        serializer = self.get_serializer(instance,many=False)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def partial_update(self, request, *args, **kwargs):
        data=self.data
        amount=data['amount']
        if int(amount)<=0:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)