from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.wishlist, name="wishlist"),
    path("add_wishlist/<int:id>", views.add_wishlist, name="add_wishlist"),
    path("delete_wishlist/<int:id>", views.delete_wishlist, name="delete_wishlist"),
    
]