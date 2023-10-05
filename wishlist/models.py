from django.db import models
from product.models import Product
from accounts.models import UserProfile

# Create your models here.

class Wishlist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
