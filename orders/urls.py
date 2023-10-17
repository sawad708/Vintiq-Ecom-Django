from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
      path('place_order/', views.place_order, name='place_order'),
      path('orderview/', views.orderview, name='orderview'),
      path('remove_order/<int:id>', views.remove_order, name='remove_order'),  
      path('cancel_order/<int:id>', views.cancel_order, name='cancel_order'),
      path('shipped/<int:id>', views.shipped, name='shipped'),
      path('delivered/<int:id>', views.delivered, name='delivered'),
      path('completed/<int:id>', views.completed, name='completed'),
      path('place_order_razorpay/', views.place_order_razorpay, name='place_order_razorpay'),
      path('return_order/<int:id>', views.return_order, name='return_order'),
      path('success/', views.success, name='success'),
      # path('wallet_payment/', views.wallet_payment, name='wallet_payment'),
    
    
]