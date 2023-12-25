from rest_framework import serializers
from . import models
from users.models import Basket

class BannerSerializer(serializers.ModelSerializer):
    thumbnail_image = serializers.ImageField(read_only=True)

    class Meta:
        model = models.Banner
        fields = "__all__"
class SubCategorySerializer(serializers.ModelSerializer):
    thumbnail_image = serializers.ImageField(read_only=True)
    class Meta:
        model = models.SubCategory
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(SubCategorySerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request", None)
        if request and request.method == "GET":
            self.fields["category"] = CategorySerializer(context=self.context)

class CategorySerializer(serializers.ModelSerializer):
    thumbnail_image = serializers.ImageField(read_only=True)

    class Meta:
        model = models.Category
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CategorySerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request", None)
        if request and request.method == "GET":
            subcategory=request.GET.get("subcategory",False)=="true"
            if subcategory:
                self.fields["subcategories"] = SubCategorySerializer(many=True,context=self.context)

class ProductSerializer(serializers.ModelSerializer):
    thumbnail_image = serializers.ImageField(read_only=True)
    basket=serializers.SerializerMethodField("get_basket")
    class Meta:
        model = models.Product
        fields = "__all__"

    def get_images(self, obj):
        images = obj.images.all()
        return images
    
    def get_basket(self,obj):
        request=self.context['request']
        basket=Basket.objects.filter(user=request.user,product=obj)
        data={}
        if basket:
            basket=basket.last()
            data['id']=basket.id
            data['amount']=basket.amount
        return data



    def __init__(self, *args, **kwargs):
        super(ProductSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request", None)
        if request and request.method == "GET":
            # self.fields["price"]=serializers.IntegerField(source="price")
            self.fields["discount"] = serializers.DictField(source="check_discount")
            category=request.GET.get("category",None)=='true'
            if category:
                self.fields["category"] = CategorySerializer(context=self.context)
            subcategory=request.GET.get("subcategory",None)=='true'
            if subcategory:
                self.fields["subcategory"] = SubCategorySerializer(context=self.context)
            images=request.GET.get("images",None)=='true'
            if images:
                self.fields["images"] = ProductImageSerializer(serializers.SerializerMethodField("get_images"),many=True,context=self.context)

class ProductImageSerializer(serializers.ModelSerializer):
    thumbnail_image = serializers.ImageField(read_only=True)

    class Meta:
        model = models.ProductImage
        fields = "__all__"

    def get_product(self, obj):
        product = obj.product
        data = {
            "id": product.id,
            "product": product.title
        }
        return data

    def __init__(self, *args, **kwargs):
        super(ProductImageSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request", None)
        if request and request.method == "GET":
            product=request.GET.get("product",None)=='true'
            if product:
                self.fields["product"] = serializers.SerializerMethodField("get_product")

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Discount
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(DiscountSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request", None)
        if request and request.method == "GET":
            category=request.GET.get("category",None)=='true'
            if category:
                self.fields["category"] = CategorySerializer(many=True,context=self.context)
            subcategory=request.GET.get("subcategory",None)=='true'
            if subcategory:
                self.fields["subcategory"] = SubCategorySerializer(many=True,context=self.context)
            products=request.GET.get("products",None)=='true'
            if products:
                self.fields["products"] = ProductSerializer(many=True,context=self.context)
