from django.shortcuts import render, redirect, HttpResponse
from .models import Address, Wallet
from orders.models import Order,Order_product
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash,logout
from django.http import HttpResponseRedirect
from product.models import Coupon
from django.conf import settings
from django.template.loader import render_to_string
import os
from xhtml2pdf import pisa






# Create your views here.
@login_required(login_url='login')
def userprofile(request):
    address = Address.objects.filter(user=request.user, is_aviliable = True)
    orders = Order.objects.filter(user=request.user).order_by('-id')
    context = {
        'address':address,
        'orders': orders
    }
    
    return render(request, 'userprofile/my-account.html', context)

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    context = {
        'orders': orders
    }
    
    return render(request, 'userprofile/my_orders.html', context)
    
@login_required(login_url='login')
def add_address(request):
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
        return redirect('userprofile')
    
    return render(request, 'userprofile/add_address.html')


@login_required(login_url='login')
def edit_address(request, id):
    address = Address.objects.filter(id=id)
    context = {
        'address':address
    }
    if request.method == "POST":
        
        name = request.POST['name']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        street = request.POST['street']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        
        user = request.user
        
        address = Address.objects.update(
            name = name,
            phonenumber = phonenumber,
            address = address,
            street = street,
            city = city,
            state = state,
            pincode = pincode,
            user = user
        )
        
        return redirect('userprofile')
    
    return render(request, 'userprofile/edit_address.html', context)


@login_required(login_url='login')
def delete_address(request, id):
    address = Address.objects.get(id=id)
    address.delete()
    # print(address,'rrrrrrrrrrrrr')
    # if address.is_aviliable == True:
    #     address.is_aviliable = False
        
    # else:
    #     address.is_aviliable = True
    return redirect('userprofile')
    
    
@login_required(login_url='login')
def edit_user(request):    
    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_firstname = request.POST.get('firstname')
        new_lastname = request.POST.get('lastname')
        new_email = request.POST.get('email')

        if (new_username != request.user.username):
            request.user.username = new_username
        if (new_firstname != request.user.first_name):
            request.user.first_name = new_firstname
        if (new_lastname != request.user.last_name):
            request.user.last_name = new_lastname
        if (new_email != request.user.email):
            request.user.email = new_email
        
        request.user.save()

        messages.success(request, 'Profile updated successfully')
        
        return redirect('userprofile') 

    return render(request, 'userprofile/edit_user.html')


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password =  request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if current_password and new_password == confirm_password:
            if request.user.check_password(current_password):
                request.user.set_password(new_password)
                request.user.save()
                # update_session_auth_hash(request, request.user)
                messages.success(request, 'Password changed successfully')
                logout(request)
                return redirect('login') 
            messages.error(request, 'Current password is incorrect')
            return HttpResponseRedirect(request.path_info)
        
        messages.error(request, 'New passwords do not match')
        return redirect('userprofile')
    
    return render(request, 'userprofile/change_password.html')


@login_required(login_url='login')
def order_view(request, id):
    orders = Order.objects.get(id=id)
    print('==========', orders)
    context = {
       'orders':orders, 
    }
   
    return render(request, 'userprofile/order_view.html', context)


@login_required(login_url='login')
def coupon(request):
    coupon_shows = Coupon.objects.all()
    context = {
        'coupon_shows':coupon_shows,
    }
    return render(request, 'userprofile/coupon.html', context)


@login_required(login_url='login')
def wallet(request):
    user = request.user
    wallet = Wallet.objects.get(user=user)
    context = {
        'wallet' : wallet,
    } 
    return render(request, 'userprofile/wallet.html', context)

def invoice(request,order_id):
    if request.method == 'POST':
        user = request.user
        address_id = request.POST.get('selected_address')

    order = Order.objects.get(id=order_id)
    order_items = Order_product.objects.filter(order=order)
    print('ddddddddddddddddddddddddddddddddd',order_items)
   
    
    context={
        'order': order,
        'order_items':order_items

    }
   
           
    
    return render(request,'userprofile/invoice.html',context)

def generate_invoice_pdf(order):
    # Render the invoice template to a string
    order_items = Order_product.objects.filter(order=order)
    invoice_html = render_to_string('userprofile/order_invoice.html', {'order': order,'order_items':order_items})
    # print(invoice_html)

    # Create a temporary file path to save the PDF
    temp_file_path = os.path.join(settings.MEDIA_ROOT, 'temp_invoice.pdf')
    # print(temp_file_path)

    # Generate the PDF using xhtml2pdf
    with open(temp_file_path, 'w+b') as file:
        pisa.CreatePDF(invoice_html, dest=file)
  

    return temp_file_path

def download_invoice(request, order_id):
    order = Order.objects.get(id=order_id)
    print('--------------------------------',order)
    invoice_path = generate_invoice_pdf(order)

    if invoice_path:
        # Open the generated PDF file in binary mode
        with open(invoice_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="RR-order-invoice-{order_id}.pdf"'

        # Delete the temporary invoice file
        os.remove(invoice_path)

        return response

    return HttpResponse('Failed to generate the invoice', status=500)

