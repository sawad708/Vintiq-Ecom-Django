from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path(" ", views.userprofile, name="userprofile"),
    path("add_address/", views.add_address, name="add_address"),
    path('my_orders/', views.my_orders, name='my_orders'),
    path("edit_user/", views.edit_user, name="edit_user"),
    path("delete_address/<int:id>", views.delete_address, name="delete_address"),
    path("change_password/", views.change_password, name="change_password"),
    path("edit_address/<int:id>", views.edit_address, name="edit_address"),
    path("order_view/<int:id>", views.order_view, name="order_view"),
    path("coupon/", views.coupon, name="coupon"),
    path("wallet/", views.wallet, name="wallet"),
    path('invoice/<int:order_id>', views.invoice, name='invoice'),
    path('order_invoice/<int:order_id>', views.download_invoice, name='order_invoice'),
    
]