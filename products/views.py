# rest imports
from rest_framework.response import Response
from rest_framework import viewsets,status,permissions
from rest_framework.decorators import action
# Local app imports
from .models import Category, SubCategory, Product, ProductImage, Discount,Banner
from .serializers import CategorySerializer, SubCategorySerializer, ProductSerializer, \
    ProductImageSerializer, DiscountSerializer,BannerSerializer
from rest_framework.views import APIView
# django
from django.db.models import Q
class SearchView(APIView):
    def get(self,request,*args,**kwargs):
        query=self.request.GET.get("query",None)
        if query:
            context={
                "request":self.request,
                'format': self.format_kwarg,
                'view': self
            }
            categories=Category.objects.filter(title__icontains=query)
            categories_serializer=CategorySerializer(categories,many=True,context=context)
            subcategories=SubCategory.objects.filter(title__icontains=query)
            subcategories_serializer=SubCategorySerializer(subcategories,many=True,context=context)
            products=Product.objects.filter(Q(title__icontains=query)|Q(description__icontains=query)|Q(price__icontains=query))
            products_serializer=ProductSerializer(products,many=True,context=context)
            data={
                "categories":categories_serializer.data,
                "subcategories":subcategories_serializer.data,
                "products":products_serializer.data
            }
            return Response({"result":data},status=status.HTTP_200_OK)
        return Response({"query":"is empty!"},status=status.HTTP_400_BAD_REQUEST)

class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

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
    permission_classes=[permissions.IsAuthenticated]

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
