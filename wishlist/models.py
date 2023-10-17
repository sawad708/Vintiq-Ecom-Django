from django.db import models
from variant.models import Variant
from accounts.models import UserProfile

# Create your models here.

class Wishlist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete= models.CASCADE)
    variant =models.ForeignKey(Variant, on_delete=models.CASCADE, null=True)
