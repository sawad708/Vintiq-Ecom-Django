from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from product.models import Coupon,Product
from orders.models import Order
from offer.models import Offer
from django.shortcuts import render

from django.shortcuts import render,redirect

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from accounts.models import UserProfile
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth import logout,get_user_model
from offer.models import Offer
from cart.models import Cart
from django.db.models import Sum,DateTimeField,Count
from django.db.models.functions import TruncMonth
import json
from datetime import datetime, timedelta
from django.db.models import Q
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import csv
from django.http import HttpResponse


# Create your views here.
@login_required(login_url='login')
def adminpannel(request):
    total_revenue = Order.objects.aggregate(total_revenue=Sum('total_price'))['total_revenue'] or 0
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    # Calculating monthly income
    monthly_income = Order.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(total_income=Sum('total_price')).order_by('month')
    # Calculate total users
    total_users = UserProfile.objects.count()
     
    payment_mode_counts = Order.objects.values('payment_method').annotate(order_count=Count('id'))

    # Extract labels and data for the transaction chart.
    labels = [item['payment_method'] for item in payment_mode_counts]
    data = [item['order_count'] for item in payment_mode_counts]  


    # Query to get the count of orders for each order status
    order_status_counts = Order.objects.values('status').annotate(order_count=Count('status'))
    

    # Extract labels and data for the chart
    order_labels = [item['status'] for item in order_status_counts]
    order_data = [item['order_count'] for item in order_status_counts]


    # Calculate the last 6 months from the current date
    today = datetime.now()
    last_six_months = [today.strftime('%B')]  # Initialize the list with the current month
    for i in range(1, 6):
        previous_month = today - timedelta(days=30*i)
        last_six_months.append(previous_month.strftime('%B'))


    # Calculate total sales for each of the last six months
    total_sales_data = []
    for i in range(6):
        start_date = today - timedelta(days=30*(i+1))
        end_date = today - timedelta(days=30*i)
        total_sales = Order.objects.filter(created_at__gte=start_date, created_at__lt=end_date).count()
        total_sales_data.append(total_sales)


    # Calculate total visitors for each of the last six months
    total_visitors_data = []
    for i in range(6):
        start_date = today - timedelta(days=30*(i+1))
        end_date = today - timedelta(days=30*i)
        total_visitors = UserProfile.objects.filter(date_joined__gte=start_date, date_joined__lt=end_date).count()
        total_visitors_data.append(total_visitors)      

 
    
    top_selling_products =Product.objects.values('product_name').annotate(sales_count=Count('product')).order_by('-sales_count')[:3]
    print(top_selling_products)
    # Create two lists to store product names and sales counts
    product_names = []

    sales_counts = []
    
    print('================',product_names,sales_counts)
    

    # Extract data from 'top_selling_products' and populate the lists
    for product in top_selling_products:
    
        shortened_name =product['product_name']
        product_names.append(shortened_name)
        sales_counts.append(product['sales_count'])

    
    context = {
       'total_revenue': total_revenue,
        'total_orders': total_orders,
        'total_products': total_products,
       
        'monthly_income': monthly_income,
        'total_users': total_users,
        
        'labels': labels,
        'data': data,
        
        'months': last_six_months,
        'total_sales_data': total_sales_data,
        'total_visitors_data': total_visitors_data, 

        'order_labels': order_labels,
        'order_data': order_data,

        

        'product_names': product_names,
        'sales_counts': sales_counts,


        }

    return render(request, 'admin_pannel/index.html',context)

@login_required(login_url='login')
def coupon_list(request):
    coupon = Coupon.objects.all()
    context = {
        'coupon':coupon,
    }
    return render(request, 'admin_order/coupon_list.html', context)


@login_required(login_url='login')
def offer_list(request):
    offers = Offer.objects.all()
    context = {
        'offers':offers,
    }
    return render(request, 'offer/list_offer.html', context)



@login_required(login_url='login')
def add_coupon(request):
    if request.method == 'POST':
        Coupon_code = request.POST['Coupon_code']
        minimum_amount = request.POST['minimum_amount']
        discount_price = request.POST['discount_price']
        expiry_date = request.POST['end_date']
        
        coupon = Coupon.objects.create(
            Coupon_code = Coupon_code,
            minimum_amount = minimum_amount,
            discount_price = discount_price,
            end_date = expiry_date
        )
        coupon.save()
        return redirect(coupon_list)
    return render(request, 'admin_order/add_coupon.html')

def edit_coupon(request, id):
    print('pppppppppppppppppppppppppppppppppppppppppp')
    if request.method == 'POST':
        Coupon_code = request.POST['Coupon_code']
        minimum_amount = request.POST['minimum_amount']
        discount_price = request.POST.get('discount_price')
        expiry_date = request.POST['end_date']
        
        coupon = Coupon.objects.filter(id=id).first()
        
        if coupon:
            coupon.Coupon_code = Coupon_code
            coupon.minimum_amount = minimum_amount
            coupon.discount_price = int(discount_price)
            coupon.end_date = expiry_date
            coupon.save()
            
        return redirect('coupon_list')

# def category(request):
#     return render(request, 'admin_user/user_list.html')

@login_required(login_url='login')
def order_views(request, id):
    orders = Order.objects.get(id=id)
    context = {
       'orders':orders, 
    }
   
    return render(request, 'admin_order/admin_order_view.html', context)



