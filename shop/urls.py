from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.shop, name="shop"),
    path('product_detailes/<int:id>/', views.product_detailes, name="product_detailes"),
     path('get_variant_price/<int:id>/', views.get_variant_price, name='get_variant_price'),
    
    
]