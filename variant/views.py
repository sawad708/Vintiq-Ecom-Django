from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Variant, VariantImage
from product.models import Product

# Create your views here.

def variant(request):
    variants = Variant.objects.all()
    context = {
        'variants':variants
    }
    return render(request, 'variant/list_variant.html', context)

def add_variant(request):
    products = Product.objects.all()
    if request.method == 'POST':
        color = request.POST['color']
        product = request.POST['product']
        price = request.POST['price']
        stock = request.POST['stock']
        images = request.FILES.getlist('images')
        
        product_instance = Product.objects.get(product_name = product, is_availiable = True)
        
        variant= Variant.objects.create(
            color = color,
            product = product_instance,
            price = price,
            stock = stock
        )
        variant.save()
        
     
        for image in images:
            VariantImage.objects.create(
                variant = variant,
                pr_images = image
            )
        return redirect('variant')
    return render(request, 'variant/add_variant.html', {'products':products})
        
        
def edit_product(request,id):
    products = Product.objects.all()
    if request.method == 'POST':
        color = request.POST['color']
        product = request.POST['product']
        price = request.POST['price']
        stock = request.POST['stock']
        images = request.FILES.getlist('images')
        
        product_instance = Product.objects.get(product_name = product, is_availiable = True)
        
        variant = Variant.objects.filter(id=id).first()
        
        if variant:
            variant.color = color
            variant.product = product_instance
            variant.price = price
            variant.stock = stock
            variant.save()
            
        return redirect(variant)