from django.contrib import admin
from .models import Products, Category

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name','product_price','product_description','product_quantity','product_image','product_category')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','slug')


admin.site.register(Products, ProductAdmin)
admin.site.register(Category, CategoryAdmin)