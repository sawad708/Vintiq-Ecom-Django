from django.shortcuts import render, redirect
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def display_user(request):
    users = UserProfile.objects.all()
    context = {'users' : users}
    return render(request, 'admin_user/user_list.html', context)

@login_required(login_url='login')
def user_block(request,id):
    user = UserProfile.objects.get(id = id)
    if user.is_active == True:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect('admin_user')


        
# def edit_user(request, id):
#     if request.method == 'POST':
#         firstname=request.POST['firstname']
#         lastname=request.POST['lastname']
#         username=request.POST['username']
#         email=request.POST['email']
       
        
#         user = UserProfile.objects.filter(id=id).first()
        
#         if user:
#             user.first_name=firstname
#             user.last_name=lastname
#             user.username=username
#             user.email=email
            
        
#             user.save()
        
#         return redirect('admin_user')   
    