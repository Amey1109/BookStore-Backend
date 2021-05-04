from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer


class CustomerCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        feilds = "__all__"
        exclude = ()
