from django.db import models
from accounts.models import Customer
from datetime import date
import datetime as DT

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

#Customer Order table

class Order(models.Model):
    PAYMENT_METHODS = (
        ("ONLINE_PAY", "Online Payment"),
        ("COD_PAY", "Cash Payment"),
    )

    order_placed_by = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_products = models.IntegerField(default=0)
    order_total = models.IntegerField(default=100)
    order_price = models.IntegerField(default=100)
    payment_mode = models.CharField(
        null=False, choices=PAYMENT_METHODS, max_length=30, default='Cash Payment')
    products = models.TextField(default="")
    address = models.CharField(max_length=20, default="")
    order_completed = models.BooleanField(default=False)
    date_of_ordering = models.DateField(default=date.today)
    date_of_delivery = models.DateField(
    default=DT.date.today() + DT.timedelta(days=7))

