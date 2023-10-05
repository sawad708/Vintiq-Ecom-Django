from django.db import models

# Create your models here.
class Category(models.Model):
    slug = models.CharField(max_length=50, unique=True)
    category_name = models.CharField(max_length=100, unique=True)
    category_description = models.TextField(max_length=300, blank=True)
    category_image = models.ImageField(upload_to="category_images/", blank=True)
    is_available = models.BooleanField(default=True)
    
    
    class meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    
    def __str__(self):
        return self.category_name