# rest imports
from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.decorators import action
# Local app imports
from .models import Category, SubCategory, Product, ProductImage, Discount
from .serializers import CategorySerializer, SubCategorySerializer, ProductSerializer, ProductImageSerializer, DiscountSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True,methods=['GET'])
    def get_products(self,request,*args, **kwargs):
        instance=self.get_object()
        # print(instance)
        products=Product.objects.filter(category=instance)
        serializer=ProductSerializer(products,many=True,context=self.get_serializer_context())
        return Response(serializer.data,status=status.HTTP_200_OK)

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    @action(detail=True, methods=['GET'])
    def get_products(self, request, *args, **kwargs):
        instance = self.get_object()
        # print(instance)
        products = Product.objects.filter(subcategory=instance)
        serializer = ProductSerializer(products, many=True, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
