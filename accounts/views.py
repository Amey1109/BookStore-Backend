from . utils.otp_utils import generateOTP, generatingOTP
from django.conf import settings

from django.shortcuts import render
from django.db import IntegrityError


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .models import Customer, OTP
import smtplib
from hashids import Hashids


from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


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
def customer_login(request):
    email    = request.data["email"]
    password = request.data["password"]
    customer = Customer.objects.get(email = email)  #it will  match customer email address from Table

    if customer.is_superuser:
        if customer.check_password(password):          #check password from table and assign a session or auth_token. 
            refresh = RefreshToken.for_user(customer)
            return Response({"status": True, "is_admin":True, "refresh":str(refresh), "access": str(refresh.access_token), "loggedIn": str(customer.username), "id": customer.pk})
        else:
            return Response({"status":False})

    else:
        if customer.check_password(password):          #check password from table and assign a session or auth_token. 
            refresh = RefreshToken.for_user(customer)
            return Response({"status": True, "is_admin":False, "refresh":str(refresh),"access": str(refresh.access_token), "loggedIn": str(customer.username), "id": customer.pk})
        else:
            return Response({"status":False})
   

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    
    id = request.data['id']
    customer_object = Customer.objects.get(id = id)
    customer_object.set_password(request.data['new_password'])
    customer_object.save()
    try:
        return Response({'msg':'password update Successfully'})
    except customer_object.DoesNotExist as e:
         return Response({"status": False, "Error ": "Customer does not exist"})


@api_view(['POST'])
def Sendemail(request):
    user_email = Customer.objects.filter(email = request.data['email']).values_list('email')
    if user_email.exists():
        sender_email = "gingertestuser1245@gmail.com"
        rec_email = user_email[0][0]
        password = "stoxvnvworbwyxcs"
        user_id = Customer.objects.filter(email = request.data['email']).values_list('id')
        gen_id = user_id[0][0]
        hashids = Hashids()
        encrypted_User_id= hashids.encode(gen_id)
        msg = MIMEMultipart('alternative')
        frontend_url =  settings.RESETPASSWORD_URL +"/ResetPassword"
        text = "Hi!\nHow are you?\nHere is the link you wanted:"
        html = '<html> <head></head> <body><p>Hi!<br> How are you?<br> Here is the  <a href="{0}/{1}">http://localhost:3000/Resetpassword</a> you wanted.</p></body></html>'.format(frontend_url, encrypted_User_id)
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)
      
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
       
        
        server.sendmail(sender_email, rec_email, msg.as_string())
        server.quit()

        return Response({'msg':'email sent','email':encrypted_User_id})
    else:
        return Response({'msg':'invalid email!'})

@api_view(['PUT'])
def password_reset(request,id):
    hashids = Hashids()
    dec_id = hashids.decode(id)
    decrypted_id = dec_id[0]
    print(decrypted_id)
    person = Customer.objects.get(id = decrypted_id)
    person.set_password(request.data['password'])
    person.save()
    try:
        return Response({'msg':'password update Successfully','id':decrypted_id})
    except Exception as e:
        print(str(e))

     
    
        






