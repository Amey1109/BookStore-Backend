from django.urls import path
from products import views


urlpatterns = [

    #product path
    path('get_products/', views.get_products),  
    path('delete_Products/', views.delete_Products), 
    path('post_products/', views.post_products),
    path('update_products/', views.update_products),

    # category path

    path('get_category/', views.get_Category), 
    path('delete_Category/', views.delete_Category),
    path('post_Category/', views.post_Category),
    path('put_Category/', views.update_Category),  

    #cart path

    path('get_cart_details/', views.get_cart_details),
    path('add_to_cart/', views.add_to_cart),
    path('remove_from_cart/', views.remove_from_cart),

     # forget password link without login
    path('coupon/', views.get_coupon),
    
    
]
