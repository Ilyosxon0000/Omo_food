from conf.views import AuthModelViewSet
from .models import Each_Product,Order
from .serializers import Each_ProductSerializer,OrderSerializer
# Create your views here.

class Each_ProductViewSet(AuthModelViewSet):
    queryset=Each_Product.objects.all()
    serializer_class=Each_ProductSerializer

class OrderViewSet(AuthModelViewSet):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    
