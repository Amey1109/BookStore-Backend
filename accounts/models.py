from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


# Custom User Which Can Login using Email address and password


# Test Password
'''
email = admin@admin.com
password = admin
'''


class Customer(AbstractUser):
    phone_number = models.IntegerField(null=True, blank=True)
    # email address is Unique for every user
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'   # uses Email  feild to Login
    REQUIRED_FIELDS = ['username']


class OTP(models.Model):
    phone_number = models.IntegerField()
    otp = models.CharField(max_length=4)
    is_verfied = models.BooleanField(default=False)
