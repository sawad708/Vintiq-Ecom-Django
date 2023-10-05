from django.shortcuts import render,get_object_or_404,redirect
from product.models import Product
from .models import Cart, Cart_item
from shop.views import shop
from django.contrib import messages
from userprofile.models import Address
from django.contrib.auth.decorators import login_required
from product.models import Coupon
from django.conf import settings
import razorpay
from variant.models import Variant

# Create your views here.

# def cart(request):
#     if request.user.is_authenticated:
#         user = request.user
        
#         cart = Cart.objects.filter(user=user).first()
#         # print('=========',cart)
#         product = Product.objects.all()
#         cart_item = Cart_item.objects.all()
        
#         if cart:
#             cart_items = cart_item.all()
#         else:
#             cart_items = []
            
#         for cart_item in cart_items:
#             quantity = cart_item.quantity
        
#             total_price = cart.get_total_price()
            
#     context = {
#         'cart':cart,
#         'cart_items':cart_items,
#         'cart_item':cart_item,
#         'product':product,
#         'quantity':quantity,
#         'total_price':total_price,
        
#     }
    
    
#     return render(request, 'cart/cart.html',context)
@login_required(login_url='login')
def cart(request):
    if request.user.is_authenticated:
        user = request.user

        # Retrieve the user's cart
        cart = Cart.objects.filter(user=user).first()
        
        # Initialize variables
        cart_items = []
        total_price = 0
        total = 0
        
        if request.method == 'POST':
            coupon_code = request.POST.get('coupon')
            cancel_coupon = request.POST.get('cancel_coupon')
            
            if coupon_code and not cancel_coupon:
                coupon_obj = Coupon.objects.filter(Coupon_code__icontains=coupon_code).first()
                
                if not coupon_obj:
                    messages.warning(request, 'Invalid Coupon')
                
                else:
                    if cart.get_total_price() < coupon_obj.minimum_amount:
                        messages.warning(request, f'The amount should be above{coupon_obj.minimum_amount}')
                    elif coupon_obj.is_expired:
                        messages.warning(request, 'Coupon is Expired')
                    elif cart.coupon and cart.coupon.is_expired:
                        messages.warning(request, 'the coupon is expired')
                    else:
                        cart.coupon = coupon_obj
                        cart.save()
                        messages.success(request, 'Coupon Applied')
            elif cancel_coupon:
                cart.coupon = None
                cart.save()
                messages.success(request, 'Coupen removed Successfully')
                
            

        if cart:
            # If the cart exists, retrieve its items and calculate the total price
            cart_items = Cart_item.objects.filter(cart=cart)
            total_price = cart.get_total_price()
            print('........',total_price)
            
            if cart.coupon:
                total = total_price - cart.coupon.discount_price
            else:
                total = total_price
            
        context = {
            'cart': cart,
            'cart_items': cart_items,
            'product': Product.objects.all(),
            'total_price': total_price,
            'total':total,
        }

        return render(request, 'cart/cart.html', context)
    else:
        # If the user is not authenticated, you can redirect them to the home page
        return redirect('home')

@login_required(login_url='login')
def add_to_cart(request,id):
    user = request.user
    variant = get_object_or_404(Variant, id=id)
    cart, _= Cart.objects.get_or_create(user=user)
    
    if not variant.is_available or variant.stock <=0 :
        
        return(shop)
    
    cart_item, created = Cart_item.objects.get_or_create(cart=cart, variant=variant)
    
    if not created:
        if variant is not None and cart_item.quantity >= variant.stock:
            messages.warning(request, 'out of stock')
            return redirect('shop')
        else:
            cart_item.quantity += 1
            cart_item.save()
            
    messages.success(request, 'added succesfully')
    return redirect('cart')
   
@login_required(login_url='login') 
def increment_cart_item(request,id):
    
    cart_item = get_object_or_404(Cart_item, id=id)
    print('............',cart_item )
    if cart_item.cart.user != request.user:
        messages.error(request, 'you do not have permision to update cart')
        return redirect('cart')
    
    if cart_item.variant is not None and cart_item.quantity >= cart_item.variant.stock:
        messages.warning(request, 'maximum quantity reached')
    else:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, 'quantity updated successfully')
    return redirect('cart')


@login_required(login_url='login')
def decrement_cart_item(request, id):
    cart_item = get_object_or_404(Cart_item, id=id)
    
    if cart_item.cart.user != request.user:
        messages.error(request, 'you do not have permision to update this item')
        return redirect('cart')
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.success(request, 'quantity updated successfully')
    else:
        messages.warning(request, 'minimum quantity reached')
        
    return redirect('cart')


@login_required(login_url='login')
def delete_cart_item(request, id):
    cart_item = get_object_or_404(Cart_item, id=id)
    
    if cart_item.cart.user != request.user:
        messages.error(request, 'you dont have permisision to delete')
        return redirect('cart')
    
    cart_item.delete()
    messages.success(request, 'item removed succesfully')
    return redirect('cart')
    


@login_required(login_url='login')
def checkout(request):
    
    user = request.user
    cart = Cart.objects.get(user=user)
    address = Address.objects.filter(user=user, is_aviliable = True)
    cart_item = Cart_item.objects.all()
    variant = Variant.objects.all()
    
    if cart:
        # cart_items = cart.cart_items.all()
        cart_items=Cart_item.objects.filter(cart=cart)

       
    else:
        cart_items = []
        
    
        
    for cart_item in cart_items:
        quantity = cart_item.quantity
        single_product_price = cart_item.get_total_price()
        total_price = cart.get_total_price()
        
        if cart.coupon:
            total = total_price - cart.coupon.discount_price
        else:
            total = total_price
            
            
    client = razorpay.Client(auth= ( settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET ))
    payment = client.order.create({'amount' :int(total) * 100 , 'currency' :'INR', 'payment_capture' : 1 })
        
    
    context = {
        'address':address,
        'cart':cart,
        # 'cart_products':cart_products,
        'cart_item':cart_items,
        'quantity':quantity,
        'variant':variant,
        'total_price':total_price,
        'single_product_price':single_product_price,
        'total':total,
        'payment':payment,
        
            
    }
        
    
    
    return render(request, 'cart/checkout.html', context)


@login_required(login_url='login')
def add_addres(request):
    if request.method == "POST":
        
        name = request.POST['name']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        street = request.POST['street']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        
        user = request.user
        
        address = Address.objects.create(
            name = name,
            phonenumber = phonenumber,
            address = address,
            street = street,
            city = city,
            state = state,
            pincode = pincode,
            user = user
        )
        address.save()
        return redirect('checkout')
    
    return render(request, 'userprofile/add_address.html')
