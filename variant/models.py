from django.db import models
from product.models import Product

# Create your models here.
class Variant(models.Model):
    color = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    stock = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    
    
    def is_outofstock(self):
        return self.stock <= 0
    
    
    
    def __str__(self):
        return self.product.product_name + " " + self.color

    


class VariantImage(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name="variant_image")
    pr_images = models.ImageField(upload_to="photos/variant")
    
    def __str__(self):
        return self.variant.color + 'image'
    