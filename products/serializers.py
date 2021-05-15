from django.db import models
from rest_framework import serializers
from . models import Category
from . models import Products
from . models import CartProduct
from . models import Coupon

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ( "id", "product_name","product_price","product_description","product_quantity","product_image","product_category")

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ( "id","name","slug")

class CartProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = "__all__"

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'