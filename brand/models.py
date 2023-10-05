from django.db import models

# Create your models here.
class Brand(models.Model):
    brand_name = models.CharField(max_length=100, unique=True)
    brand_description = models.TextField(max_length=300, blank=True)
    brand_image = models.ImageField(upload_to='photos/brand')
    is_availiable = models.BooleanField(default=True)
    
    
    