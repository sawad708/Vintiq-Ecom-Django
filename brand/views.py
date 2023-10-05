from django.shortcuts import render,redirect
from .models import Brand
from PIL import Image
from django.contrib.auth.decorators import login_required

# from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.
@login_required(login_url='login')
def list_brand(request):
    brands = Brand.objects.all()
    context = {'brands':brands}
    return render(request, 'brand/brand_list.html', context)


@login_required(login_url='login')
def add_brand(request):
    if request.method == "POST":
        brand_name = request.POST['name']
        brand_description = request.POST['description']
        brand_image = request.FILES.get('image')
        
        brand = Brand.objects.create(
            brand_name = brand_name,
            brand_description = brand_description,
            brand_image = brand_image
        )
        brand.save()
        return redirect('brand')
    return render(request, 'brand/add_brand.html') 


@login_required(login_url='login')
def edit_brand(request, id):
    
    if request.method == 'POST':
        brand_name = request.POST['name']
        brand_description = request.POST['description']
        brand_image = request.FILES.get('image', None)
        
        brand = Brand.objects.filter(id=id).first()  # Use .first() to get a single object
        
        if brand:
            brand.brand_name = brand_name
            brand.brand_description = brand_description
            
            if brand_image is not None:
                brand.brand_image = brand_image
            
            brand.save()  # Save the changes
        
        
        return redirect('brand')


@login_required(login_url='login')    
def block_brand(request,id):
    brand = Brand.objects.get(id=id)
    if brand.is_availiable == True:
        brand.is_availiable = False
    else:
        brand.is_availiable = True
    brand.save()
    return redirect('brand')
    
    
# def block_brand(request, brand_id):
#     brand = get_object_or_404(Brand, id=brand_id)
    
#     if request.method == 'POST':
#         # Toggle the 'is_availiable' status
#         brand.is_availiable = not brand.is_availiable
#         brand.save()
        
#         return redirect('brand')  # Redirect to admin brand list
    
#     return render(request, 'brand/list_brand.html', {'brand': brand})
    
    
        
    