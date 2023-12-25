# rest import
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
# local import
from users.serializers import CustomUserSerializer
from conf.views import AuthModelViewSet
from .models import Each_Product,Order,Delivery,Location
from .serializers import Each_ProductSerializer,OrderSerializer,CheckOutSerializer,DeliverySerializer,LocationSerializer
# Create your views here.
# import djoser

class DeliveryViewSet(AuthModelViewSet):
    queryset=Delivery.objects.all()
    serializer_class=DeliverySerializer

class LocationViewSet(AuthModelViewSet):
    queryset=Location.objects.all()
    serializer_class=LocationSerializer

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
        validated_data = {**serializer.validated_data, **kwargs}
        serializer.create(validated_data)
        
        # # user update
        # serializer = CustomUserSerializer(self.get_user(), data=self.data['user'], partial=True)
        # serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)
        #
        # serializer.location.save()


        return Response({"data":serializer.data},status=status.HTTP_200_OK)

    @action(detail=True,methods=['PATCH'])
    def change_delivery_status(self,request,*args,**kwargs):
        instance=self.get_object()
        delivery_status=self.data.pop('delivery_status')
        serializer=self.get_serializer(instance,data={"delivery_status":delivery_status},partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)