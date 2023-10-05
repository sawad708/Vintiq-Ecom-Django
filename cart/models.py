from django.db import models
from accounts.models import UserProfile
from product.models import Coupon
from variant.models import Variant


# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=True)
    
    def get_total_price(self):
        total_price = sum(item.get_total_price() for item in self.cart_items.all())
        return total_price
    
    
class Cart_item(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    
    def get_total_price(self):
        if self.variant is not None:
            return self.variant.price * self.quantity
        