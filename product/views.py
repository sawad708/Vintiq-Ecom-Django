from django.shortcuts import render, redirect
from .models import Product
from django.contrib import messages
from brand.models import Brand
from category.models import Category
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    brands = Brand.objects.all()
    categories = Category.objects.filter(is_available=True)
    context = {
        'products' : products,
        'brands':brands,
        'categories':categories
         
    }
    return render(request, 'product/product_list.html', context)


def add_product(request):
    brands=Brand.objects.filter(is_availiable=True)
    categories = Category.objects.filter(is_available=True)
    context= {
        'brands':brands,
        'categories':categories
        }
    if request.method == "POST":
        image = ''
        try:
            image = request.FILES['image']
        except:
            if image == '':
                messages.info(request, "image feild can't be empty")
                return redirect(add_product)
            
        name = request.POST['name']
        brand = request.POST['brand']
        category = request.POST['category']
        description = request.POST['description']
        

        brand_instance = Brand.objects.get(brand_name=brand, is_availiable=True)
        category_instance = Category.objects.get(id=category, is_available=True)
            
        product=Product.objects.create(
                product_name = name,
                brand = brand_instance,
                category = category_instance,
                description = description,
                image = image,
                
                
                
        )
        product.save()
        return redirect(products)
    return render(request, 'product/product.html', context)
        
        
def edit_product(request, id):

    if request.method == "POST":
        name = request.POST['name']
        brand = request.POST['brand']
        category = request.POST['category']
        description = request.POST['description']
        
        brand_instance =Brand.objects.get(brand_name=brand, is_availiable=True)
        
        category_instance = Category.objects.get(id=category, is_available  =True)
        
        product = Product.objects.filter(id=id).first()
        
        if product:
            product.product_name = name
            product.brand = brand_instance
            product.category = category_instance
            product.description = description
            product.save()
            
        return redirect('product')
    

    
# def delete_product(request, id):
#     product = Product.objects.get(id=id)
#     product.delete()
#     return redirect('product')

def block_product(request, id):
    product = Product.objects.get(id=id)
    if product.is_availiable == True:
        product.is_availiable = False
    else:
        product.is_availiable = True
    product.save()
    return redirect('product')


