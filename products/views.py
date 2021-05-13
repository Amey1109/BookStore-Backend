from django.shortcuts import render

from .models import Products,Category
from .serializers import ProductSerializer,CategorySerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory



# Create your views here.
@api_view(['GET'])
def get_products(request):
        query_set = Products.objects.all()
        serializer_object = ProductSerializer(query_set, many=True)

        return Response(serializer_object.data)

@api_view(['POST'])
def post_products(request):
        new_products =  request.data
        serializer_object = ProductSerializer(data = new_products)
        
        if serializer_object.is_valid():
            serializer_object.save()
            return Response({"message":"post successfully"})
        else:
            return Response(serializer_object.errors)

@api_view(['PUT'])
def update_products(request):
        updated_products = Products.objects.get(id=request.data["id"])
        serializer_object = ProductSerializer(updated_products, request.data)

        if serializer_object.is_valid():
            serializer_object.save()
            return Response({"mesage":"data updated successfully"})
        else:
            return Response(serializer_object.errors)

@api_view(['DELETE'])
def delete_Products(request):
    id = request.data["id"]

    updated_products = Products.objects.get(id = id)

    updated_products.delete()
    return Response({"msg":"deleted successfully"})

## category functionality

@api_view(['GET'])
def get_Category(request):
        query_set = Category.objects.all()
        serializer_object = CategorySerializer(query_set, many=True)

        return Response(serializer_object.data)



@api_view(['DELETE'])
def delete_Category(request):
    id = request.data["id"]

    updated_Category = Category.objects.get(id = id)

    updated_Category.delete()
    return Response({"msg":"deleted successfully"})

@api_view(['POST'])
def post_Category(request):
        new_products =  request.data
        serializer_object = CategorySerializer(data = new_products)
        
        if serializer_object.is_valid():
            serializer_object.save()
            return Response({"message":"post successfully"})
        else:
            return Response(serializer_object.errors)

@api_view(['PUT'])
def update_Category(request):
        updated_category = Category.objects.get(id=request.data["id"])
        serializer_object = CategorySerializer(updated_category, request.data)

        if serializer_object.is_valid():
            serializer_object.save()
            return Response({"mesage":"data updated successfully"})
        else:
            return Response(serializer_object.errors)


