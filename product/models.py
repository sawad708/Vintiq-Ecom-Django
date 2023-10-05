from django.db import models
from brand.models import Brand
from category.models import Category
from offer.models import Offer

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="photos/categories")
    is_availiable = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.product_name
    
    
    
    
class Coupon(models.Model):
    Coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    end_date = models.DateField(null=True)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)