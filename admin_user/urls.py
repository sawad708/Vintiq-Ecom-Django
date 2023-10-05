from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_user, name="admin_user"),
    path('user_block/<int:id>/', views.user_block, name='user_block'),
    # path('edit_user/<int:id>/', views.edit_user, name='edit_user'),
]