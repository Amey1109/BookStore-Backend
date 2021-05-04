import os
import random
import math

# * Generating 4-Digit Random Numbers


def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


# *Checks OTP with the otp recevied from the GET Request
def generatingOTP(number):
    #number_with_code = "+91"+number
    OTP = generateOTP()

    #! Code for Twilio
    # account_sid = 'AC6593b5edf2aaa3acfcb8e796bd76fd55'
    # auth_token = 'eff74dbf93b705721502f7fc4a4dbe3f'
    # client = Client(account_sid, auth_token)

    # message = client.messages \
    #                 .create(
    #                     body="Thank you for Registering on GFL your OTP is "+OTP,
    #                     from_='+12082617126',
    #                     to=number_with_code
    #                 )

    return OTP
