from django.shortcuts import render

from .models import Products,Category,Customer,Cart,CartProduct
from .serializers import ProductSerializer,CategorySerializer,CartProductSerializers
from django.http.response import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
# get all the products
@api_view(['GET'])
def get_products(request):
        query_set = Products.objects.all()
        serializer_object = ProductSerializer(query_set, many=True)

        return Response(serializer_object.data)

#insert the product
@api_view(['POST'])
def post_products(request):
        new_products =  request.data
        serializer_object = ProductSerializer(data = new_products)
        
        if serializer_object.is_valid():
            serializer_object.save()
            return Response({"message":"post successfully"})
        else:
            return Response(serializer_object.errors)

#update the products
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
#get all category
@api_view(['GET'])
def get_Category(request):
        query_set = Category.objects.all()
        serializer_object = CategorySerializer(query_set, many=True)

        return Response(serializer_object.data)


#delete the category of product
@api_view(['DELETE'])
def delete_Category(request):
    id = request.data["id"]

    updated_Category = Category.objects.get(id = id)

    updated_Category.delete()
    return Response({"msg":"deleted successfully"})

#insert the category of products
@api_view(['POST'])
def post_Category(request):
        new_products =  request.data
        serializer_object = CategorySerializer(data = new_products)
        
        if serializer_object.is_valid():
            serializer_object.save()
            return Response({"message":"post successfully"})
        else:
            return Response(serializer_object.errors)

#update the category of product
@api_view(['PUT'])
def update_Category(request):
        updated_category = Category.objects.get(id=request.data["id"])
        serializer_object = CategorySerializer(updated_category, request.data)

        if serializer_object.is_valid():
            serializer_object.save()
            return Response({"mesage":"data updated successfully"})
        else:
            return Response(serializer_object.errors)
#view cart of the user
@api_view(['POST'])
def get_cart_details(request):
    query_set = CartProduct.objects.filter(user=request.data['id'])
    print(request.data)
    product_data = []
    result = []
    price = 0
    for item in query_set:
        price = price + item.product.product_price
        product_data.append({
            'product_name': item.product.product_name,
            'product_price': item.product.product_price,
        })

    result.append(
        {
            'cart_owner_id': item.user.id,
            'cart_owner_name': item.cart.user_id.username,
            'product': product_data,
            'cart_price': price
        }
    )

    return JsonResponse(result, safe=False)

#add product to the cart
@api_view(['POST'])
def add_to_cart(request):
    try:
        cart_user = Cart.objects.get(user_id=request.data['id'])
        user_instance = Customer.objects.get(id=request.data['id'])
        product_instance = Products.objects.get(id=request.data['product_id'])
        cart = CartProduct(user=user_instance,
        product=product_instance, cart=cart_user)
        cart.save()
        return Response({"msg": "Item added to the Cart"})

    except Cart.DoesNotExist as e:
        user_instance = Customer.objects.get(id=request.data['id'])
        new_cart_user = Cart(user_id=user_instance)
        new_cart_user.save()
        user_instance = Customer.objects.get(id=request.data['id'])
        product_instance = Products.objects.get(id=request.data['product_id'])
        cart = CartProduct(user=user_instance,
                           product=product_instance, cart=new_cart_user)
        cart.save()
        return Response({"msg": "Item added to the Cart "})

#Remove product from  cart
@csrf_exempt
@api_view(['POST'])
def remove_from_cart(request):
    user_instance = Customer.objects.get(id=request.data['id'])
    cart_user = Cart.objects.get(user_id=user_instance)
    product_instance = Products.objects.get(id=request.data['product_id'])

    cart = CartProduct.objects.filter(
        user=user_instance, product=product_instance, cart=cart_user)
    cart.delete()
    return Response({"msg": "Item Deleted"})

#Coupon functionality for user
@api_view(['POST'])
def get_coupon(request):
        code = request.data['code']
        user_objects = Coupon.objects.filter(code=code)
        serializer_object = CouponSerializer(user_objects, many=True)
        return Response(serializer_object.data)


