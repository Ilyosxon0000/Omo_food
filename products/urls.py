# rest 
from rest_framework.routers import DefaultRouter
from products.views import CategoryViewSet, SubCategoryViewSet, ProductViewSet, ProductImageViewSet, DiscountViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="categories")
router.register("sub-categories", SubCategoryViewSet, basename="sub-categories")
router.register("products", ProductViewSet, basename="products")
router.register("product-images", ProductImageViewSet, basename="product-images")
router.register("discounts", DiscountViewSet, basename="discount")