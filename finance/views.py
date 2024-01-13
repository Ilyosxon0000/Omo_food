from rest_framework import viewsets
from finance.models import Product,Order
from finance.serializers import FinanceProductSerializer,FinanceOrderSerializer
# Create your views here.

class ProductView(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=FinanceProductSerializer

class OrderView(viewsets.ModelViewSet):
    queryset=Order.objects.all()
    serializer_class=FinanceOrderSerializer
