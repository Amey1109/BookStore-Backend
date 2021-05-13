from django.urls import path
from products import views


urlpatterns = [
    path('get_products/', views.get_products),  # Generates the OTP
    path('delete_Products/', views.delete_Products), 
    path('post_products/', views.post_products),
    path('update_products/', views.update_products),

    path('get_category/', views.get_Category), 
    path('delete_Category/', views.delete_Category),
    path('post_Category/', views.post_Category),
    path('put_Category/', views.update_Category),  
    
]
