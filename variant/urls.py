from django.urls import path
from . import views


urlpatterns = [
    path('', views.variant, name="variant"),
    path('add_variant/', views.add_variant, name='add_variant'),
    # path('edit_product/<int:id>', views.edit_product, name='edit_product'),
   
    
]
