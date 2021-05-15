from django.contrib import admin
from .models import Products, Category, CartProduct, Cart, Coupon

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name','product_price','product_description','product_quantity','product_image','product_category')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','slug')


class CartProductAdmin(admin.ModelAdmin):
    list_display=("id","user","product","cart")

class CouponAdmin(admin.ModelAdmin):
    list_display = ("id","code","discount")


admin.site.register(Products, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CartProduct, CartProductAdmin)
admin.site.register(Cart)
admin.site.register(Coupon,CouponAdmin)