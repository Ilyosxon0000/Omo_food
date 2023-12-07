# django
from django.urls import path,include
# rest 
from rest_framework.routers import DefaultRouter
from products.views import CategoryViewSet, SubCategoryViewSet, ProductViewSet, ProductImageViewSet, DiscountViewSet
from users.views import CustomUserViewSet,BasketViewSet

# simple_jwt
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

products_router = DefaultRouter()
# Products 
products_router.register("categories", CategoryViewSet, basename="categories")
products_router.register("sub-categories", SubCategoryViewSet, basename="sub-categories")
products_router.register("products", ProductViewSet, basename="products")
products_router.register("product-images", ProductImageViewSet, basename="product-images")
products_router.register("discounts", DiscountViewSet, basename="discount")
# Users
users_router = DefaultRouter()
users_router.register("users", CustomUserViewSet, basename="users")
users_router.register("basket", BasketViewSet, basename="basket")

urlpatterns=[
    path('',include(products_router.urls)),
    path('',include(users_router.urls)),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
urlpatterns+=products_router.urls