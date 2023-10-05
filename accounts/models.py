from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class UserProfile(AbstractUser):
    phone_number= models.CharField(max_length=50, blank=True, null=True)
    is_block = models.BooleanField(default=False)
    user_token = models.UUIDField(default=uuid.uuid4, editable=False)
    otp_secret = models.CharField(max_length=16, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
    