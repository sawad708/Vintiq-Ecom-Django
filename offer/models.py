from django.db import models
from django.utils import timezone

# Create your models here.
class Offer(models.Model):
    title = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    discount_persentage = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
    is_delete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title