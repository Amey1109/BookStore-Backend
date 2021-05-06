from django.urls import path, include
from accounts import views

from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
urlpatterns = [
    path('generate_otp/', views.generate_otp),  # Generates the OTP
    path('check_otp/', views.check_otp),  # Checks the OTP Generated OTP

    # Register Normal Customer
    path('register_customer/', views.register_customer),

    # Register Admin with Admin rights
    path('register_admin/', views.register_admin),
    
    # Updates the registered customers
    path('update_customer/', views.update_customer),

    # Admin and Customer Login
    path('customer_login/', views.customer_login),

     # User change password 
    path('change_password/', views.change_password),

    path('token/', TokenObtainPairView.as_view(), name= 'token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
   

     # forget password link without login
    path('Sendemail/', views.Sendemail),

    # reset password through email
    path('password_reset/', views.password_reset),
]
