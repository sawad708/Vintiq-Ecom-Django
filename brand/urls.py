from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_brand, name="brand"),
    path('add_brand/', views.add_brand, name='add_brand'),
    path('edit_brand/<int:id>/', views.edit_brand, name='edit_brand'),
    # path('block-brand/<int:brand_id>/', views.block_brand, name='block_brand'),
    path('block_brand/<int:id>/', views.block_brand, name='block_brand'),
    
    
]

