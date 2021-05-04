from . utils.otp_utils import generateOTP, generatingOTP

from django.shortcuts import render
from django.db import IntegrityError


from .models import Customer, OTP

from rest_framework.response import Response
from rest_framework.decorators import api_view


# Generates the OTP and sends to the mobile number
@api_view(['POST'])
def generate_otp(request):
    number = request.data['number']
    generatedOTP = generatingOTP(number)  # Generates the 4-Digit OTP
    if generatedOTP:
        data = OTP(phone_number=number, otp=generatedOTP)
        data.save()
        print(generatedOTP)
        return Response({"isOTPSent": True})
    else:
        return Response({"isOTPSent": False})


@api_view(['PUT'])
def check_otp(request):

    # validations for Checking if the request.data has what we need
    if 'number' in request.data:
        number = request.data['number']
    else:
        return Response({"Error": "Expected phone number in request body not present"})

    if 'otp' in request.data:
        otp = request.data['otp']
    else:
        return Response({"Error": "Expected OTP in request body not present"})


    generatedOTP = OTP.objects.filter(
        phone_number=number).values_list('otp')
    if generatedOTP[0][0] == otp:       #
        try:
            data = OTP.objects.get(phone_number=number)

        except OTP.DoesNotExist as error:
            return Response({"Error": error})

        data.is_verfied = True
        data.save()
        return Response({"status": True})
    else:
        return Response({"status": False})
