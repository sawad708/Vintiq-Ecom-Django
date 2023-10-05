from django.shortcuts import render,redirect, get_object_or_404
from product.models import Product
from brand.models import Brand
from category.models import Category
from variant.models import Variant 
from django.http import JsonResponse

# Create your views here.
def shop(request):
    variants = Variant.objects.all()
    # product = Product.objects.filter(is_availiable=True)
    products= Product.objects.filter(is_availiable=True,product__isnull=False).distinct()

    
    
    
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')
    
    if category_id:
        products = variants.filter(product__category__id = category_id, product__is_availiable=True)
        
    if brand_id:
        products = Variant.objects.filter(product__brand__id=brand_id, product__is_availiable=True)
        
    # if request.method == 'POST':
    #     searched = request.POST['searched']
    #     products = Product.objects.filter(product_name = searched)
    #     return render(request, 'shop/shop.html', {'products':products})
        
   
    brands = Brand.objects.filter(is_availiable=True)
    categories = Category.objects.filter(is_available=True)
    context = {
        'products':products,
        'categories':categories,
        'brands':brands,
        'variants':variants
        
        }
    
    
    
    return render(request, 'shop/shop.html', context)

def product_detailes(request, id):
    
    variants = Variant.objects.filter(id=id)
    # products = get_object_or_404(Product, id=id)
    # variants = products.product.all()
    # variant = products.product.all()
    print('---------------',variants)
    # variant_img = []
    # first = variants.first()
    # variant_img1 = []
    # for variant in variants:
    #     variant_img.extend(variant.variant_image.all())
        
    # for variant in variants:
    #     variant_img.extend(variant.variant_image.all())
    # print('-------------------',variant_img)
    # variant = Variant.objects.all(product = variants.product )
    context = {
        # 'products':products,
        'variants':variants,
        # 'variant': variant
        # 'variant_img':variant_img,
        # 'first':first,

        
    }
    return render(request, 'shop/product_detailes.html', context)

def get_variant_price(request, id):
    try:
        variant = Variant.objects.get(id=id)
        return JsonResponse({'success': True, 'price': variant.price})
    except Variant.DoesNotExist:
        return JsonResponse({'success': False})    