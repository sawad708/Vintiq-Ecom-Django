from django.shortcuts import render, get_object_or_404, redirect
from . models import Wishlist
from variant.models import Variant

# Create your views here.

def wishlist(request):
    user = request.user
    wishlists = Wishlist.objects.filter(user=user)
    return render(request, 'wishlist/wishlist.html', {'wishlists':wishlists})
    
    
def add_wishlist(request, id):
    user = request.user
    variant = get_object_or_404(Variant, id=id)
    wishlist, _ = Wishlist.objects.get_or_create(user=user, variant=variant)
    
    if Wishlist.objects.filter(user=user, variant=variant).exists():
        # Handle the case where the product is already in the wishlist, e.g., display a message
        return redirect('wishlist')
    
    wishlist = Wishlist(user=user, variant=variant)
    wishlist.save()
    
    return redirect('shop')


def delete_wishlist(request, id):
    wishlist = get_object_or_404(Wishlist, id=id)
    wishlist.delete()
    
    return redirect('wishlist')
    
    