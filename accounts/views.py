from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from hashids import Hashids
import smtplib
from .models import Customer, OTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .serializers import AddressSerializer,PincodeSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer, OTP, Address,Pincode
from . utils.otp_utils import generateOTP, generatingOTP
from django.conf import settings

from django.shortcuts import render
from django.db import IntegrityError

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
        serializer_object = AddressSerializer(query_set, many=True)
        if query_set:
            return Response(serializer_object.data)
        else:
            return Response({"status":False,"message":"Address does not exist for user"})
    except Customer.DoesNotExist as e:
        return Response({"status": false, "message": "Customer does not exist"})


@api_view(['POST'])
def customer_login(request):
    email = request.data["email"]
    password = request.data["password"]
    # it will  match customer email address from Table
    customer = Customer.objects.get(email=email)

    if customer.is_superuser:
        # check password from table and assign a session or auth_token.
        if customer.check_password(password):
            refresh = RefreshToken.for_user(customer)
            return Response({"status": True, "is_admin": True, "refresh": str(refresh), "access": str(refresh.access_token), "loggedIn": str(customer.username), "id": customer.pk})
        else:
            return Response({"status": False})

    else:
        # check password from table and assign a session or auth_token.
        if customer.check_password(password):
            refresh = RefreshToken.for_user(customer)
            return Response({"status": True, "is_admin": False, "refresh": str(refresh), "access": str(refresh.access_token), "loggedIn": str(customer.username), "id": customer.pk})
        else:
            return Response({"status": False})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):

    id = request.data['id']
    customer_object = Customer.objects.get(id=id)
    customer_object.set_password(request.data['new_password'])
    customer_object.save()
    try:
        return Response({'msg': 'password update Successfully'})
    except customer_object.DoesNotExist as e:
        return Response({"status": False, "Error ": "Customer does not exist"})


@api_view(['POST'])
def send_email(request):
    user_email = Customer.objects.filter(
        email=request.data['email']).values_list('email')
    if user_email.exists():
        sender_email = "gingertestuser1245@gmail.com"
        rec_email = user_email[0][0]
        password = "stoxvnvworbwyxcs"
        user_id = Customer.objects.filter(
            email=request.data['email']).values_list('id')
        gen_id = user_id[0][0]
        hashids = Hashids()
        encrypted_User_id = hashids.encode(gen_id)
        msg = MIMEMultipart('alternative')
        frontend_url = settings.RESETPASSWORD_URL + "/ResetPassword"
        text = "Hi!\nHow are you?\nHere is the link you wanted:"
        html = '<html> <head></head> <body><p>Hi!<br> How are you?<br> Here is the  <a href="{0}/{1}">http://localhost:3000/Resetpassword</a> you wanted.</p></body></html>'.format(
            frontend_url, encrypted_User_id)
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)

        server.sendmail(sender_email, rec_email, msg.as_string())
        server.quit()

        return Response({'msg': 'email sent', 'email': encrypted_User_id})
    else:
        return Response({'msg': 'invalid email!'})


@api_view(['PUT'])
def password_reset(request, id):
    hashids = Hashids()
    dec_id = hashids.decode(id)
    decrypted_id = dec_id[0]
    print(decrypted_id)
    person = Customer.objects.get(id=decrypted_id)
    person.set_password(request.data['password'])
    person.save()
    try:
        return Response({'msg': 'password update Successfully', 'id': decrypted_id})
    except Exception as e:
        print(str(e))

        query_set = Address.objects.filter(customer_id=id)
        if query_set:
            serializer_object = AddressSerializer(query_set, many=True)
            return Response({"Address": serializer_object.data, "status": True, "message": "Address Exists"})
        else:
            return Response({"status": False, "message": "Address does not exist for the requested user"})
    except Customer.DoesNotExist as e:
        return Response({"status": false, "message": "Customer does not exist"})




##pincode functionality
@api_view(['PUT'])
def get_Pincode(request):
    if 'pincode' in request.data:
          pincode = request.data['pincode']
    else:
      return Response({"Error": "pincode is not provided"})
    
    if 'generatedpincode':
        generatedpincode = Pincode.objects.get(pincode = pincode)

        generatedpincode.is_verified =True
        generatedpincode.save()
        return Response({"True": "we deliver our goodies on this pincode"})
    else:
        return Response({"False": "sorry we couldnt deliver our goodies on this Pincode "})

@api_view(['DELETE'])
def delete_Pincode(request):
    id = request.data["id"]

    updated_Category = Pincode.objects.get(id = id)

    updated_Category.delete()
    return Response({"msg":"deleted successfully"})

@api_view(['POST'])
def post_Pincode(request):
        new_pincode =  request.data
        serializer_object = PincodeSerializer(data = new_pincode)
        
        if serializer_object.is_valid():
            serializer_object.save()
            return Response({"message":"post successfully"})
        else:
            return Response(serializer_object.errors)

@api_view(['PUT'])
def update_Pincode(request):
        updated_pincode = Pincode.objects.get(id=request.data["id"])
        serializer_object = PincodeSerializer(updated_pincode, request.data)

        if serializer_object.is_valid():
            serializer_object.save()
            return Response({"mesage":"data updated successfully"})
        else:
            return Response(serializer_object.errors)



    
