from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_categories, name="category"),
    path('add_category/', views.add_category, name='add_category'),
    # path('delete_category/<int:id>/', views.delete_category, name='delete_category'),
    path('edit_category/<int:id>/', views.edit_category, name='edit_category'),
    path('block_category/<int:id>/', views.block_category, name='block_category'),
]

