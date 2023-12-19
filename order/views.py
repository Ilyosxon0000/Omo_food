# rest import
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
# local import
from users.serializers import CustomUserSerializer
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
    @property
    def data(self):
        request=self.request
        data={}
        if type(request.data)==dict:
            data=dict(request.data)
        else:
            data={key: None if value == 'null' else value for key, value in request.data.items()}
        data['client_user']=self.get_user().id
        return data

    def get_serializer_class(self):
        if self.action=="checkout":
            return CheckOutSerializer
        return super().get_serializer_class()

    @action(detail=False,methods=["POST"])
    def checkout(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        # # user update
        # serializer = CustomUserSerializer(self.get_user(), data=self.data['user'], partial=True)
        # serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)
        #
        # serializer.location.save()


        return Response({"data":serializer.data},status=status.HTTP_200_OK)
