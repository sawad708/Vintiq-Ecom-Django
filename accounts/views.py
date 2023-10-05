from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from . models import UserProfile
from django.contrib import messages
from django.core.mail import send_mail
import random
from django.utils import timezone
from datetime import timedelta
from admin_user.views import display_user
from admin_user.views import user_block
from django.http import HttpResponse


# Create your views here.

def login(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,  user)
            return redirect('/')
        else:
            messages.info(request, "invalid Login")
            return redirect('login')
        
        
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
    
            firstname=request.POST['firstname']
            lastname=request.POST['lastname']
            username=request.POST['username']
            email=request.POST['email']
            password=request.POST['password']
            password1=request.POST['password1']
            
            if UserProfile.objects.filter(username=username).exists():
                messages.info(request, "username already exists")
                return redirect('register')
            
            if UserProfile.objects.filter(email=email).exists():
                messages.info(request, "email already exists")
                return redirect('register')
            
            if not firstname.isalnum():
                messages.error(request, 'user name must be alpha-numeric')
                return redirect('register')

            if not isinstance(firstname,str):
                messages.error(request, 'user name must be charactor')
                return redirect('register')
            
            if not lastname.isalnum():
                messages.error(request, 'user name must be alpha-numeric')
                return redirect('register')

            if not isinstance(lastname,str):
                messages.error(request, 'user name must be charactor')
                return redirect('register')

            if not username:
                messages.error(request, 'please enter the user name')
                return redirect('register')
        
            if not email:
                messages.error(request, 'please enter the user email')
                return redirect('register')
            
            if not username.isalnum():
                messages.error(request, 'user name must be alpha-numeric')
                return redirect('register')

            if not isinstance(username,str):
                messages.error(request, 'user name must be charactor')
                return redirect('register')

            if password!=password1:
                messages.error(request, 'check your password')
                return redirect('register')
            
            user = UserProfile.objects.create_user(
                first_name=firstname,
                last_name=lastname,
                username=username,
                email=email,
                password=password,
                
            )
            # otp generation and send otp
            otp_secret = generate_otp(user)
            send_otp_email(email, otp_secret)
            # store Otp secret in session
            request.session['otp_secret'] = otp_secret
            context = {'email':email}
            return render(request,'accounts/otp_login.html',context)
            
              
    return render(request, 'accounts/register.html')



def verify_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = UserProfile.objects.filter(email=email).last()
        user_otp = request.POST.get('otp')
        otp_secret = request.session.get('otp_secret')
        if otp_secret:
            
            if otp_secret == user_otp:  
                user.is_verified = True
                user.save()
                
                
                # clear otp feilds
                
                
                del request.session['otp_secret']
                return redirect('login')
            else:
                error_message = "Invalid OTP. please Try again"
        else:
            error_message = "OTP has Expired or invalid. please request a new OTP."
        return render(request, 'accounts/otp_login.html', {'error_message' : error_message})
    return render(request, 'accounts/otp_login.html')
        
    

# to generate otp
def generate_otp(user):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    user.otp_secret =otp
    user.otp_verified = False
    user.save()
    return otp

# sending email
def send_otp_email(email, otp_secret):
    send_mail(
        'OTP verification',
        f'Your OTP for registration : {otp_secret}',
        'muhammad.sawad0048@gmail.com',
        [email],
        fail_silently=False,
    )
    



    
    
    
# def clear_user_otp(user):
#     user.otp_secret = None
#     user.save()

def logout(request):
    auth.logout(request)
    return redirect('/')

def userblock(request,id):
    if not request.user.is_superuser:
        return redirect('home')
    
    