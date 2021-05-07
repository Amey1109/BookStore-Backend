from . utils.otp_utils import generateOTP, generatingOTP

from django.shortcuts import render
from django.db import IntegrityError


from .models import Customer, OTP, Address

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .serializers import AddressSerializer


# Generates the OTP and sends to the mobile number
@api_view(['POST'])
def generate_otp(request):
    if 'number' in request.data:  # Checks whether the nuber is present in the request body
        # checks weather the number present in the request body is of 10-Digit
        if len(request.data['number']) == 10:
            number = request.data['number']
        else:
            return Response({"Error": "Mobile Number should be of 10-digits", "isOTPSent": False})
    else:
        return Response({"Error": "Expected phone number in request body not present", "isOTPSent": False})

    generatedOTP = generatingOTP(number)  # Generates the 4-Digit OTP
    if generatedOTP:
        data = OTP(phone_number=number, otp=generatedOTP)
        data.save()
        print(generatedOTP)
        return Response({"isOTPSent": True})
    else:
        return Response({"isOTPSent": False})

# Checks the OTP generated for corresponding Phone Number


@api_view(['PUT'])
def check_otp(request):
    # validations for Checking if the request.data has what we need
    if 'number' in request.data:
        if len(request.data['number']) == 10:
            number = request.data['number']
        else:
            return Response({"Error": "Mobile Number should be of 10-digits", "checkStatus": False})
    else:
        return Response({"Error": "Expected phone number in request body not present", "checkStatus": False})

    if 'otp' in request.data:
        otp = request.data['otp']
    else:
        return Response({"Error": "Expected OTP in request body not present", "checkStatus": False})

    generatedOTP = OTP.objects.filter(
        phone_number=number).values_list('otp')
    if generatedOTP[0][0] == otp:       #
        try:
            data = OTP.objects.get(phone_number=number)

        except OTP.DoesNotExist as error:
            return Response({"Error": error})

        data.is_verfied = True
        data.save()
        return Response({"checkStatus": True})
    else:
        return Response({"checkStatus": False})

# Register Normal User


@api_view(['POST'])
def register_customer(request):
    if 'username' in request.data:
        user_name = request.data['username']
    else:
        return Response({"Error": "Username Not Provided"})

    if 'fname' in request.data:
        fname = request.data['fname']
    else:
        return Response({"Error": "First Name not Provided"})

    if 'lname' in request.data:
        lname = request.data['lname']
    else:
        return Response({"Error": "Last Name not Provided"})

    if 'email' in request.data:
        email = request.data['email']
    else:
        return Response({"Error": "Email Not Provided"})

    if 'number' in request.data:
        phone_number = request.data['number']
    else:
        return Response({"Error": "Contact Number Not Provided"})

    if 'password' in request.data:
        password = request.data['password']
    else:
        return Response({"Error": "Password Not Provided"})

    customer = Customer(email=email)
    customer.username = user_name
    customer.phone_number = phone_number
    customer.first_name = fname
    customer.last_name = lname
    customer.set_password(password)

    try:
        customer.save()
        try:
            otp_clutter = OTP.objects.get(phone_number=phone_number)

            if otp_clutter.is_verfied:
                otp_clutter.delete()
            else:
                return Response({"Error": "Mobile Number Not Verified"})
        except OTP.DoesNotExist as e:
            return Response({"Error": "Mobile Does Not Exists"})

        return Response({"registerStatus": True, "IntegrityError": False})
    except IntegrityError as e:
        return Response({"registerStatus": False, "IntegrityError": True})


# Registers Admin
@api_view(['POST'])
def register_admin(request):
    if 'username' in request.data:
        user_name = request.data['username']
    else:
        return Response({"Error": "Username Not Provided"})

    if 'fname' in request.data:
        fname = request.data['fname']
    else:
        return Response({"Error": "First Name not Provided"})

    if 'lname' in request.data:
        lname = request.data['lname']
    else:
        return Response({"Error": "Last Name not Provided"})

    if 'email' in request.data:
        email = request.data['email']
    else:
        return Response({"Error": "Email Not Provided"})

    if 'number' in request.data:
        phone_number = request.data['number']
    else:
        return Response({"Error": "Contact Number Not Provided"})

    if 'password' in request.data:
        password = request.data['password']
    else:
        return Response({"Error": "Password Not Provided"})

    admin = Customer.objects.create_superuser(
        username=user_name, email=email, first_name=fname, last_name=lname, phone_number=phone_number, password=password)
    try:
        admin.save()
        try:
            otp_clutter = OTP.objects.get(phone_number=phone_number)

            if otp_clutter.is_verfied:
                otp_clutter.delete()
            else:
                return Response({"Error": "Mobile Number Not Verified"})
        except OTP.DoesNotExist as e:
            return Response({"Error": "Mobile Does Not Exists"})

        return Response({"registerStatus": True, "IntegrityError": False})
    except IntegrityError as e:
        return Response({"registerStatus": False, "IntegrityError": True})


@api_view(['PUT'])
def update_customer(request):
    id = request.data['id']
    if 'username' in request.data:
        new_user_name = request.data['username']
    else:
        return Response({"Error": "Username Not Provided"})

    if 'fname' in request.data:
        new_fname = request.data['fname']
    else:
        return Response({"Error": "First Name not Provided"})

    if 'lname' in request.data:
        new_lname = request.data['lname']
    else:
        return Response({"Error": "Last Name not Provided"})

    if 'email' in request.data:
        email = request.data['email']
    else:
        return Response({"Error": "Email Not Provided"})

    if 'number' in request.data:
        new_phone_number = request.data['number']
    else:
        return Response({"Error": "Contact Number Not Provided"})

    if 'password' in request.data:
        new_password = request.data['password']
    else:
        return Response({"Error": "Password Not Provided"})

    try:
        customer = Customer.objects.get(id=id)
        customer.username = new_user_name
        customer.phone_number = new_phone_number
        customer.first_name = new_fname
        customer.last_name = new_lname
        customer.set_password(new_password)
        customer.save()
        return Response({"status": True})

    except Customer.DoesNotExist as e:

        return Response({"status": False, "Error ": "Customer does not exist"})


@api_view(['POST'])
def add_address(request):
    if 'customer_id' in request.data:
        customer_id = request.data['customer_id']
    else:
        return Response({"Error": "Expected 'Customer ID' "})

    if 'address' in request.data:
        address = request.data['address']
    else:
        return Response({"Error": "Expected 'Address' "})

    serializer_object = AddressSerializer(data=request.data)
    if serializer_object.is_valid():
        serializer_object.save()
        return Response({"status": True, "message": "Address added successfully"})
    else:
        return Response(serializer_object.errors)


@api_view(['PUT'])
def update_address(request):

    if 'id' in request.data:
        id = request.data['id']
    else:
        return Response({"Error": "Expected 'Address ID' "})

    if 'customer_id' in request.data:
        customer_id = request.data['customer_id']
    else:
        return Response({"Error": "Expected 'Customer ID' "})

    if 'address' in request.data:
        address = request.data['address']
    else:
        return Response({"Error": "Expected 'Address' "})

    try:
        address_to_be_updated = Address.objects.get(id=id)
        serializer_object = AddressSerializer(
            address_to_be_updated, request.data)
        if serializer_object.is_valid():
            serializer_object.save()
            return Response({"status": True, "message": "Address updated successfully"})
        else:
            return Response(serializer_object.errors)

    except Address.DoesNotExist as e:
        return Response({"status": false, "message": "Address does not exist"})


@api_view(["GET"])
def get_address(request, id):
    try:
        query_set = Address.objects.filter(customer_id=id)
        if query_set:
            serializer_object = AddressSerializer(query_set, many=True)
            return Response({"Address": serializer_object.data, "status": True, "message": "Address Exists"})
        else:
            return Response({"status": False, "message": "Address does not exist for the requested user"})
    except Customer.DoesNotExist as e:
        return Response({"status": false, "message": "Customer does not exist"})
