from rest_framework import serializers
from . models import Category, Products

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ( "id", "product_name","product_price","product_description","product_quantity","product_image","product_category")

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ( "id","name","slug")