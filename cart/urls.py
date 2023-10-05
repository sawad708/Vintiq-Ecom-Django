from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
      path('cart/', views.cart, name='cart'),
      path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
      path('increment_cart_item/<int:id>', views.increment_cart_item, name='increment_cart_item'),
      path('decrement_cart_item/<int:id>', views.decrement_cart_item, name='decrement_cart_item'),
      path('checkout', views.checkout, name='checkout'),
      path('delete_cart_item/<int:id>', views.delete_cart_item, name='delete_cart_item'),
      path("add_addres/", views.add_addres, name="add_addres"),
    
    
]