from django.db import models
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import Transpose
from django.contrib.auth.models import User

# User.objects.make_random_password()

class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(editable=False)
    image = models.FileField(upload_to="images/categories/%y%m%d", blank=True, null=True)
    thumbnail_image = ImageSpecField(
        source = 'image',
        processors = [Transpose(),],
        format = 'JPEG',
        options = {'quality':30}
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(editable=False)
    image = models.FileField(upload_to="images/subcategories/%y%m%d", blank=True, null=True)
    thumbnail_image = ImageSpecField(
        source = 'image',
        processors = [Transpose(),],
        format = 'JPEG',
        options = {'quality':30}
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Product(models.Model):
    MEASURE_TYPE = (
        ("kg", "kg"),
        ("litr", "litr"),
        ("dona", "dona"),
        ("metr", "metr")
    )
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, related_name="products", on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=1000, decimal_places=2, blank=True, null=True)
    amount = models.FloatField(default=0)
    amount_measure = models.CharField(max_length=25, choices=MEASURE_TYPE, default="kg")
    created_date = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to="images/products/%y%m%d")
    thumbnail_image = ImageSpecField(
        source = 'image',
        processors = [Transpose(),],
        format = 'JPEG',
        options = {'quality':30}
    )


    def check_discount(self):
        all_discount=Discount.objects.filter(is_active=True,products_status="ALL")
        product_discount=self.discounts.filter(is_active=True)
        product_many_discount=self.discount_many.filter(is_active=True)
        category_discount=self.category.discounts.filter(is_active=True)
        subcategory=self.subcategory
        subcategory_discount=subcategory.discounts.filter(is_active=True) if subcategory else subcategory

        discount=None
        discount_price=self.price
        data={}

        if all_discount:
            discount=all_discount[0]
            discount_price=discount.discount_price_product(self)
        elif product_discount:
            discount=product_discount[0]
            discount_price=discount.discount_price_product(self)
        elif product_many_discount:
            discount=product_many_discount[0]
            discount_price=discount.discount_price_product(self)
        elif category_discount:
            discount=category_discount[0]
            discount_price=discount.discount_price_product(self)
        elif subcategory_discount:
            discount=subcategory_discount[0]
            discount_price=discount.discount_price_product(self)
        else:
            return data
        
        from .serializers import DiscountSerializer
        discount_serializer=DiscountSerializer(discount,many=False)
        data=discount_serializer.data
        data['product_discount_price']=discount_price
        return data

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.FileField(upload_to="images/products/%y%m%d")
    thumbnail_image = ImageSpecField(
        source = 'image',
        processors = [Transpose(),],
        format = 'JPEG',
        options = {'quality':30}
    )

    def __str__(self):
        return self.product.title


class Discount(models.Model):
    PRODUCTS_STATUS=(
        ("ALL","ALL"),
        ("CUSTOM","CUSTOM"),
    )
    title = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    products_status=models.CharField(max_length=25,choices=PRODUCTS_STATUS,default="CUSTOM")
    product = models.ForeignKey(Product, related_name="discounts", on_delete=models.CASCADE, blank=True,null=True)
    products = models.ManyToManyField(Product, related_name="discount_many", blank=True)
    category = models.ManyToManyField(Category, related_name="discounts", blank=True)
    subcategory = models.ManyToManyField(SubCategory, related_name="discounts", blank=True)
    
    def discount_price_product(self,product):
        price=product.price
        current_price=price-((price/100)*self.value)
        return current_price

    def __str__(self):
        return self.title
    
"""
discount
    start date 
    end date
    foiz
    products(manytomany) blank true
    category(manytomany) blank true
    subcategory(manytomany) blank true
    products_status (tanlanganlarga, barcha maxsulotlarga)
    discount_status (fixed chegirma, dinamik chegirma % )
    
"""


