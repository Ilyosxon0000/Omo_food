# rest import
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
# local import
from conf.views import AuthModelViewSet
from .models import Each_Product,Order
from .serializers import Each_ProductSerializer,OrderSerializer,CheckOutSerializer
# Create your views here.
# import djoser

class Each_ProductViewSet(AuthModelViewSet):
    queryset=Each_Product.objects.all()
    serializer_class=Each_ProductSerializer

class OrderViewSet(AuthModelViewSet):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer

    def get_serializer_class(self):
        if self.action=="checkout":
            return CheckOutSerializer
        return super().get_serializer_class()

    @action(detail=False,methods=["POST"])
    def checkout(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)
