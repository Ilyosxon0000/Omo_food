# rest 
from rest_framework.routers import DefaultRouter
# local import
from finance.views import ProductView,OrderView

router = DefaultRouter()
router.register("finance_products", ProductView, basename="finance_products")
router.register("finance_orders", OrderView, basename="finance_orders")