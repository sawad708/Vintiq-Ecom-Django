from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.products, name="product"),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    # path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('block_product/<int:id>/', views.block_product, name='block_product'),
    
]

