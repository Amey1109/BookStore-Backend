from django.db import models
from accounts.models import Customer

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=225)
    slug = models.SlugField(unique=True, blank=True, null=True)

class Products(models.Model):
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=20)
    product_image = models.ImageField(upload_to='product_images/')
    product_price = models.IntegerField(blank=True, null=True)
    product_quantity = models.IntegerField(blank=True, null=True)
    product_description = models.TextField()

    def __str__(self):
            return self.product_name

##Cart Related Stuff
class Cart(models.Model):
    user_id  = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    products = models.ManyToManyField(Products, through='CartProduct')

    def __str__(self):
        return self.user_id.username

class CartProduct(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + self.product.product_name 

# Discount Coupon for user

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.FloatField(max_length=15) 

    def __str__(self):
        return self.code
