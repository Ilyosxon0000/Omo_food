# rest import
from rest_framework import serializers
# local import
from .models import Delivery,Each_Product,Location,Order
from users.models import Basket
from users.serializers import CustomUserSerializer
from products.serializers import ProductSerializer

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model=Delivery
        fields="__all__"
class Each_ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Each_Product
        fields="__all__"

    def __init__(self, *args, **kwargs):
        super(Each_ProductSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request", None)
        if request and request.method == "GET":
            product=request.GET.get("product")=="true"
            if product:
                self.fields["product"] = ProductSerializer(many=False,context=self.context)

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Location
        fields="__all__"

class OrderSerializer(serializers.ModelSerializer):
    # delivery_status_enum=serializers.
    class Meta:
        model=Order
        fields="__all__"
    def __init__(self, *args, **kwargs):
        super(OrderSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request", None)
        if request and request.method == "GET":
            each_products=request.GET.get("each_products")=="true"
            if each_products:
                self.fields["each_products"] = Each_ProductSerializer(many=True,context=self.context)
            delivery=request.GET.get("delivery")=="true"
            if delivery:
                self.fields["delivery"] = DeliverySerializer(many=False,context=self.context)
            location=request.GET.get("location")=="true"
            if location:
                self.fields["location"] = LocationSerializer(many=False,context=self.context)
            user=request.GET.get("user")=="true"
            if user:
                self.fields["user"] = CustomUserSerializer(many=False,context=self.context)
            

class UserRegistrationSerializer(serializers.Serializer):
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    phone=serializers.CharField()

class CheckOutSerializer(serializers.Serializer):
    basket_products=serializers.ListField(child = serializers.IntegerField())
    user=UserRegistrationSerializer()
    location=LocationSerializer()
    delivery=serializers.IntegerField()
    payment_method=serializers.ChoiceField(choices=Order.PAYMENT_METHODS)

    def create(self, validated_data):
        basket_products = validated_data.pop('basket_products')
        delivery = validated_data.pop('delivery')
        payment_method = validated_data.pop('payment_method')
        user=validated_data.pop("user")
        location=validated_data.pop("location")
        request=self.context.get("request",None)

        user = CustomUserSerializer(request.user, data=user, partial=True)
        user.is_valid(raise_exception=True)
        user=user.save()

        each_products=[]

        order_total_price=0

        for basket_product_id in basket_products:
            basket_product=Basket.objects.get(id=basket_product_id)
            product=basket_product.product
            if basket_product.amount>product.amount:
                basket_product.objects.update(amount=product.amount)
            amount=basket_product.amount
            basket_total_price=basket_product.get_total_price()
            total_price=basket_total_price['discount_price'] if basket_total_price.get("discount_price", None) else basket_total_price['price']
            each_product=Each_Product.objects.create(
                product=product,
                amount=amount,
                total_price=total_price
            )
            order_total_price+=total_price
            each_products.append(each_product.id)
            product.amount-=amount
            product.save()
            basket_product.delete()

        location=LocationSerializer(data=location)
        location.is_valid(raise_exception=True)
        location=location.save()

        order_total_price+=Delivery.objects.get(id=delivery).price

        data={
            "location":location.id,
            "user":user.id,
            "each_products":each_products,
            "total_price":order_total_price,
            "delivery":delivery,
            "payment_method":payment_method,
        }

        serializer = OrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return serializer