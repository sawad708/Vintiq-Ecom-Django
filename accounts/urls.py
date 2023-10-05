from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name="login"),
    path('register/', views.register, name='register'),
    path('verify-otp/>', views.verify_otp, name='verify_otp'),
    path('logout/', views.logout, name="logout")
    
]