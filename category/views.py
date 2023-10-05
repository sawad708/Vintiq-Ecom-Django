from django.shortcuts import render,redirect
from .models import Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def list_categories(request):
    categories = Category.objects.all()
    context = {'categories':categories}
    return render(request, 'category/category_list.html', context)


@login_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        slug = request.POST['slug']
        category_name = request.POST['name']
        category_description = request.POST['description']
        category_image = request.FILES.get('cropped_image')


        # Check for empty fields
        if not slug or not category_name or not category_description:
            messages.info(request, 'Some fields are empty')
        else:
            # Check for duplicate category name or slug
            if Category.objects.filter(category_name=category_name).exists():
                messages.info(request, 'Category name already exists')
            elif Category.objects.filter(slug=slug).exists():
                messages.info(request, 'Slug already exists')
            else:
                # Create the category
                category = Category(
                    slug=slug,
                    category_name=category_name,
                    category_description=category_description,
                    category_image=category_image,
                    is_available=True
                )
                category.save()
                messages.success(request, 'Category created successfully')
                return redirect(list_categories)
    else:
        messages.info(request, 'Use the form to create a category')

    return render(request, 'category/add_category.html')




@login_required(login_url='login')
def edit_category(request, id):
    if request.method == 'POST':
        slug = request.POST['slug']
        category_name = request.POST['name']
        category_description = request.POST['description']
        category_image = request.FILES.get('image', None)
        
        category = Category.objects.filter(id=id).first()
        
        if category:
            category.slug = slug
            category.category_name = category_name
            category.category_description =category_description
            
            if category_image is not None:
                category.category_image = category_image
                
            category.save()
            
        return redirect('category')
                

# def delete_category(request,id):
#     category = Category.objects.get(id=id)
#     category.delete()
#     return redirect(list_categories)


@login_required(login_url='login')
def block_category(request, id):
    category = Category.objects.get(id=id)
    if category.is_available == True:
        category.is_available = False
    else:
        category.is_available = True
    category.save()
    return redirect('category')