from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.adminpannel, name="admin_pannel"),
    path('coupon_list/', views.coupon_list, name="coupon_list"),
    path('offer_list/', views.offer_list, name="offer_list"),
    path('add_coupon/', views.add_coupon, name="add_coupon"),
    path('edit_coupon/<int:id>', views.edit_coupon, name="edit_coupon"),
    # path('category/', views.category, name="category"),
    path('admin_user/', include('admin_user.urls')),
    path('category/', include('category.urls')),
    path('brand/', include('brand.urls')),
    path('product/', include('product.urls')),
    path('variant/', include('variant.urls')),
    path('order_views/<int:id>', views.order_views, name="order_views"),
    # path('offer/', include('offer.urls')),
    
]