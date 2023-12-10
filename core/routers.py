# django
from django.urls import path,include

# simple_jwt
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# local import
from products.urls import router as products_router
from users.urls import router as users_router
from order.urls import router as orders_router

urlpatterns=[
    path('',include(products_router.urls)),
    path('',include(users_router.urls)),
    path('',include(orders_router.urls)),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]