from django.db import models
from accounts.models import UserProfile
from userprofile.models import Address
from product.models import Coupon
from variant.models import Variant

# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'pending'),
        ('PROCESSING', 'processing'),
        ('SHIPPED', 'shipped'),
        ('DELIVERED', 'delivered'),
        ('CANCELLED', 'cancelled'),
        ('CONFIRMED', 'confirmed'),
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name='orders',  null=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True,blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,default=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=50)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tracking_no = models.CharField(max_length=150, null=False)
    
    def get_orderIttem_count(self):
        count = sum(item.quantity for item in self.orderitems.all())
        return count
    
    def calculate_total_price(self):
        total_price =sum(item.variant.price * item.quantity for item in self.orderitems.all())
        return total_price
    


class Order_product(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    def calculated_item_total(self):
        return self.variant.price * self.quantity
    

    