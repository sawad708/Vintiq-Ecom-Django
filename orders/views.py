from django.shortcuts import render,get_object_or_404,redirect
from userprofile.models import Address,Wallet
from cart.models import Cart
from .models import Order, Order_product
import random
from datetime import datetime,timedelta
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal
from django.contrib.auth.decorators import login_required


# Create your views here.

# ========================================================== admin side ==============================================================


@login_required(login_url='login')
def orderview(request):
    
    orders = Order.objects.all().order_by('-id')
    return render(request, 'admin_order/admin-orders.html',{'orders':orders})


@login_required(login_url='login')
def remove_order(request, id):
    order = get_object_or_404(Order, id=id)
    
    order_items = Order_product.objects.all()
    for order_item in order_items:
        product = order_item.product
        product.stock += order_item.quantity
        product.save()
        
    order.status = 'cancelled'
    order.save()
    
    messages.warning(request, 'order has been cancelled and deleted succesfully')
    
    return redirect('orderview')


@login_required(login_url='login')
def shipped(request, id):
    order = get_object_or_404(Order, id=id)
    
    order.status = 'shipped'
    order.save()
    
    return redirect('orderview')


@login_required(login_url='login')
def delivered(request, id):
    order = get_object_or_404(Order, id=id)
    
    order.status = 'delivered'
    order.save()
    
    return redirect('orderview')


@login_required(login_url='login')
def completed(request, id):
    order = get_object_or_404(Order, id=id)
    
    order.status = 'completed'
    order.save()
    
    return redirect('orderview')


# ============================================================ end of admin side ======================================================

# def order_detailes(request):
    
#     ord = Order_product.objects.filter(order__user = request.user,).order_by('order__created_at')
#     return render(request, '', {'order':ord})
    
    
    
@login_required(login_url='login')
def place_order(request):
    if request.method == 'POST':
        user = request.user
        print(user,'----999999999999999999')
        address_id = request.POST.get('selected_address')  
        print('--------',address_id)
        
        if not address_id:
            user_addresses = Address.objects.filter(user=user)
            error_message = 'please select an address to proceed'
            return render(request, 'cart/checkout.html', {'user_addresses':user_addresses, 'error_message': error_message})
        
        selected_address = get_object_or_404(Address, id = address_id, user=user)
       

        
        payment_method = 'COD'
        
        user_cart = Cart.objects.filter(user=user).last()
        print('$$$$$$',user_cart)
        if not user_cart:
            
            return redirect('home')
        
        if user_cart.coupon:
            total = user_cart.get_total_price() - user_cart.coupon.discount_price
        else:
            total= user_cart.get_total_price()
       
        
        new_order = Order()
        new_order.user = user
        new_order.address = selected_address
        new_order.payment_method = payment_method
        new_order.sub_total = user_cart.get_total_price()
        new_order.coupon = user_cart.coupon
        new_order.total_price = total
        track_no = 'RR'+ str(random.randint(111111,999999))
        while Order.objects.filter(tracking_no=track_no).exists():
            track_no = 'RR'+str(random.randint(111111,999999))
            
        new_order.tracking_no = track_no
        new_order.save()
        
        return_deadline = datetime.now() + timedelta(days=14)
        
        new_order.return_deadline = return_deadline
        new_order.save()
        
        cart_items = user_cart.cart_items.all()
        
        for cart_item in cart_items:
            order_item = Order_product()
            order_item.order = new_order
            order_item.variant = cart_item.variant
            order_item.price = total
            order_item.quantity = cart_item.quantity
            
            order_item.save()
            
            
            cart_item.variant.stock -= cart_item.quantity
            cart_item.variant.save()
            
        user_cart.delete()
        
        new_order.status = 'confirmed'
        new_order.save()
        
        context = {
            'new_order':new_order,
        }
        return render(request, 'orders/place_order.html', context)
    
    user_addresses = Address.objects.filter(user=request.user)   
    return render(request, 'cart/checkout.html',{'user_addresses':user_addresses})


@login_required(login_url='login')
def place_order_razorpay(request):
    print('hello')
    if request.method == 'POST':
        user = request.user
        print(user,'----999999999999999999')
        address_id = request.POST.get('address')  
        print('--------',address_id)
        
        if not address_id:
            user_addresses = Address.objects.filter(user=user)
            error_message = 'please select an address to proceed'
            return render(request, 'cart/checkout.html', {'user_addresses':user_addresses, 'error_message': error_message})
        
        selected_address = get_object_or_404(Address, id = address_id, user=user)
        
        payment_method = 'Razorpay'
        
        user_cart = Cart.objects.filter(user=user).last()
        
        print('$$$$$$',user_cart)
        if not user_cart:
            
            return redirect('home')
        
        if user_cart.coupon:
            total = user_cart.get_total_price() - user_cart.coupon.discount_price
        else:
            total= user_cart.get_total_price()
       
        
        new_order = Order()
        new_order.user = user
        new_order.address = selected_address
        new_order.payment_method = payment_method
        new_order.sub_total = user_cart.get_total_price()
        new_order.coupon = user_cart.coupon
        new_order.total_price = total
        track_no = 'RR'+ str(random.randint(111111,999999))
        while Order.objects.filter(tracking_no=track_no).exists():
            track_no = 'RR'+str(random.randint(111111,999999))
            
        new_order.tracking_no = track_no
        new_order.save()
        
        return_deadline = datetime.now() + timedelta(days=14)
        
        new_order.return_deadline = return_deadline
        new_order.save()
        
        cart_items = user_cart.cart_items.all()
        
        for cart_item in cart_items:
            order_item = Order_product()
            order_item.order = new_order
            order_item.variant = cart_item.variant
            order_item.price = total
            order_item.quantity = cart_item.quantity
            
            order_item.save()
            
            
            cart_item.variant.stock -= cart_item.quantity
            cart_item.variant.save()
            
        user_cart.delete()
        
        new_order.status = 'confirmed'
        new_order.save()
        
        context = {'new_order': new_order}
        # return render(request, 'orders/place_order.html',{ 'order' : new_order.id})
        print('-----------', new_order.id)    
        return JsonResponse({'status': 'Your order has been placed successfully.', 'order': new_order.id})

    print('-----------', new_order.id)    
       

        
        
    user_addresses = Address.objects.filter(user=request.user)   
    context = {'new_order': new_order} 
    
    return render(request, 'cart/checkout.html',{'user_addresses':user_addresses})
    


# def place_order_razorpay(request):
#     new_order = None  # Initialize new_order to None

#     if request.method == 'POST':
#         user = request.user
#         address_id = request.POST.get('selected_address')

#         if not address_id:
#             user_addresses = Address.objects.filter(user=user)
#             error_message = 'Please select an address to proceed.'
#             return render(request, 'cart/checkout.html', {'user_addresses': user_addresses, 'error_message': error_message})

#         selected_address = get_object_or_404(Address, id=address_id, user=user)

#         payment_method = 'Razorpay'

#         user_cart = Cart.objects.filter(user=user).last()

#         if not user_cart:
#             return redirect('home')

#         if user_cart.coupon:
#             total = user_cart.get_total_price() - user_cart.coupon.discount_price
#         else:
#             total = user_cart.get_total_price()

#         new_order = Order()
#         new_order.user = user
#         new_order.address = selected_address
#         new_order.payment_method = payment_method
#         new_order.sub_total = user_cart.get_total_price()
#         new_order.coupon = user_cart.coupon
#         new_order.total_price = total
#         track_no = 'RR' + str(random.randint(111111, 999999))
#         while Order.objects.filter(tracking_no=track_no).exists():
#             track_no = 'RR' + str(random.randint(111111, 999999))

#         new_order.tracking_no = track_no
#         new_order.save()

#         return_deadline = datetime.now() + timedelta(days=14)
#         new_order.return_deadline = return_deadline
#         new_order.save()

#         cart_items = user_cart.cart_items.all()

#         for cart_item in cart_items:
#             order_item = Order_product()
#             order_item.order = new_order
#             order_item.product = cart_item.product
#             order_item.price = total
#             order_item.quantity = cart_item.quantity

#             order_item.save()

#             cart_item.product.stock -= cart_item.quantity
#             cart_item.product.save()

#         user_cart.delete()

#         new_order.status = 'confirmed'
#         new_order.save()
        
#         print(new_order,'==================================')
#         return JsonResponse({'status': 'Your order has been placed successfully.', 'order': new_order.payment_id})

#     user_addresses = Address.objects.filter(user=request.user)
#     context = {'new_order': new_order}

#     return render(request, 'cart/checkout.html', {'user_addresses': user_addresses, 'new_order': new_order})

    
@login_required(login_url='login')
def cancel_order(request, id):
    order = get_object_or_404(Order, id=id)
    user = request.user
    order_items = order.orderitems.all()
    user_wallet, _= Wallet.objects.get_or_create(user=user)
    
    if order.payment_method == 'Razorpay':
        for order_item in order_items:
            variant= order_item.variant
            variant.stock += order_item.quantity
            variant.save()
            
        
        user_wallet.balance += Decimal(str(order.total_price)) # Assuming total_amount is the order total
        user_wallet.save()
        
        
    for order_item in order_items:
        variant = order_item.variant
        variant.stock += order_item.quantity
        variant.save()
        
    order.status = 'cancelled'
    order.save()
    
    messages.warning(request, 'order has been cancelled and deleted succesfully')
    
    return redirect('userprofile')       



@login_required(login_url='login')
def return_order(request, id):
    order_item = Order_product.objects.get(id=id)
    
    order_item.order.status = 'return'
    product     = order_item.variant
    print('wwwwwwwwwww',product)
    product.stock += order_item.quantity
    product.save()
    order_item.order.save()
    
    return redirect('userprofile')


@login_required(login_url='login')
def success(request):
    user = request.user
    new_order=Order.objects.filter(user=user).last()
    context = {
        'new_order':new_order
    }
    return render(request, 'orders/place_order.html', context)

def invoice(request, id):
    invoice = get_object_or_404(Order, id=id)
    
    return render(request,'',{'invoice':invoice})

    
    
def wallet_payment(request):
    print('hello')
    if request.method == 'POST':
        user = request.user
        print(user,'----999999999999999999')
        address_id = request.POST.get('address')  
        print('--------',address_id)
        
        if not address_id:
            user_addresses = Address.objects.filter(user=user)
            error_message = 'please select an address to proceed'
            return render(request, 'cart/checkout.html', {'user_addresses':user_addresses, 'error_message': error_message})
        
        selected_address = get_object_or_404(Address, id = address_id, user=user)
        
        payment_method = 'Wallet'
        
        user_cart = Cart.objects.filter(user=user).last()
        print('$$$$$$',user_cart)
        if not user_cart:
            
            return redirect('home')
        
        if user_cart.coupon:
            total = user_cart.get_total_price() - user_cart.coupon.discount_price
        else:
            total= user_cart.get_total_price()
        
        wallet = Wallet.objects.get(user=user)

        if wallet <= total:
            new_order = Order()
            new_order.user = user
            new_order.address = selected_address
            new_order.payment_method = payment_method
            new_order.sub_total = user_cart.get_total_price()
            new_order.coupon = user_cart.coupon
            new_order.total_price = total
            track_no = 'RR'+ str(random.randint(111111,999999))
            while Order.objects.filter(tracking_no=track_no).exists():
                track_no = 'RR'+str(random.randint(111111,999999))
                
            new_order.tracking_no = track_no
            new_order.save()
            
            return_deadline = datetime.now() + timedelta(days=14)
            
            new_order.return_deadline = return_deadline
            new_order.save()
            
            cart_items = user_cart.cart_items.all()
            
            for cart_item in cart_items:
                order_item = Order_product()
                order_item.order = new_order
                order_item.variant = cart_item.variant
                order_item.price = total
                order_item.quantity = cart_item.quantity
                
                order_item.save()
                
                
                cart_item.variant.stock -= cart_item.quantity
                cart_item.variant.save()
                
            user_cart.delete()
            
            new_order.status = 'confirmed'
            new_order.save()
            
            context = {
                'new_order':new_order,
            }
        else:
            # messages.alert()
            return('checkout')
        
        return render(request, 'orders/place_order.html', context)