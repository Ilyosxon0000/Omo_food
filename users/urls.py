# rest 
from rest_framework.routers import DefaultRouter
# local import
from users.views import CustomUserViewSet,BasketViewSet

# Users
router = DefaultRouter()
router.register("users", CustomUserViewSet, basename="users")
router.register("basket", BasketViewSet, basename="basket")
