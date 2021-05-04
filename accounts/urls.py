from django.urls import path, include
from accounts import views
urlpatterns = [
    path('generate_otp/', views.generate_otp),
    
    path('check_otp/', views.check_otp),
]
