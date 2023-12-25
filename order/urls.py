# rest 
from rest_framework.routers import DefaultRouter
# local import
from order.views import Each_ProductViewSet,OrderViewSet,DeliveryViewSet,LocationViewSet
router = DefaultRouter()
router.register("each-products", Each_ProductViewSet, basename="each-products")
router.register("orders", OrderViewSet, basename="orders")
router.register("deliveries", DeliveryViewSet, basename="deliveries")
router.register("locations", LocationViewSet, basename="locations")