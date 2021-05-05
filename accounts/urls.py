from django.urls import path, include
from accounts import views
urlpatterns = [
    path('generate_otp/', views.generate_otp),  # Generates the OTP
    path('check_otp/', views.check_otp),  # Checks the OTP Generated OTP

    # Register Normal Customer
    path('register_customer/', views.register_customer),

    # Register Admin with Admin rights
    path('register_admin/', views.register_admin),

    # Updates the registered customers
    path('update_customer/', views.update_customer),

    path('add_address/', views.add_address), #add an address
    path('update_address/', views.update_address), #update the existing address
    path('get_address/<int:id>', views.get_address),# get all the address related to the particular customer


]
