from django.shortcuts import render, get_object_or_404, redirect
from . models import Wishlist
from product.models import Product

# Create your views here.

def wishlist(request):
    user = request.user
    wishlists = Wishlist.objects.filter(user=user)
    return render(request, 'wishlist/wishlist.html', {'wishlists':wishlists})
    
    
def add_wishlist(request, id):
    user = request.user
    product = get_object_or_404(Product, id=id)
    wishlist, _ = Wishlist.objects.get_or_create(user=user, product=product)
    
    if Wishlist.objects.filter(user=user, product=product).exists():
        # Handle the case where the product is already in the wishlist, e.g., display a message
        return redirect('wishlist')
    
    wishlist = Wishlist(user=user, product=product)
    wishlist.save()
    
    return redirect('shop')


def delete_wishlist(request, id):
    wishlist = get_object_or_404(Wishlist, id=id)
    wishlist.delete()
    
    return redirect('wishlist')
    
    