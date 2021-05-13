from django.db import models

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
