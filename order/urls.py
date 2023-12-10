# rest 
from rest_framework.routers import DefaultRouter
from order.views import Each_ProductViewSet,OrderViewSet
router = DefaultRouter()
# Products 
router.register("each-products", Each_ProductViewSet, basename="each-products")
router.register("orders", OrderViewSet, basename="orders")