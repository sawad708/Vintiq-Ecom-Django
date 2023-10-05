from django.db import models
from accounts.models import UserProfile 
    
    

class Address(models.Model):
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='addresses')
    name= models.CharField(max_length=225, null=True, blank=True)
    phonenumber = models.CharField(max_length=50)
    address = models.CharField(max_length=225,null='True')
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    is_aviliable = models.BooleanField(default=True)

class Wallet(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)