from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from userlog import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
# from django.utils.encoding import force_text
from .tokens import generate_token

# Create your views here.


def index(request):
    # return HttpResponse("Sazzad ul alam")
    return render(request, "auth/index.html")


def signup(request):

    if request.method == "POST":
        # username = request.POST.get('u_name')
        user_name = request.POST['u_name']
        first_name = request.POST['f_name']
        last_name = request.POST['l_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['c_password']

        if User.objects.filter(username=user_name):
            messages.error(request, "Username already exist! Please try some other username.")
            # return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            # return redirect('home')
        
        if len(user_name)>12:
            messages.error(request, "Username must be under 12 charcters!!")
            # return redirect('home')
        
        if password != confirm_password:
            messages.error(request, "Passwords didn't matched!!")
            # return redirect('home')
        
        if not user_name.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            # return redirect('home')
        
        myuser = User.objects.create_user(user_name, email, password)
        myuser.first_name = first_name
        myuser.last_name = last_name

        myuser.is_active = True
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # # Welcome Email**********************************************************************************************************************************************
        subject = "Welcome to GFG- Django Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to GFG!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nAnubhav Madhav"        
        from_email = settings.EMATL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        #***************************************************************************************************************************************************************
        
        # # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email Django App Login!!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('signin')



    return render(request, "auth/signup.html")


def signin(request):

    if request.method == 'POST':
        user_name = request.POST['u_name']
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(username=user_name, password=password, email=email)
        if user is not None:
            login(request, user)
            first_name = user.first_name
            return render(request, "auth/home.html", {'first_name': first_name})

        else:
            messages.error(request, "Somethings is wrong in Sign In.")
            # return redirect('index')
    
    return render(request, "auth/signin.html")


def signout(request):
    logout(request)
    messages.success(request, " Sign out Successfully!" )
    return redirect('index')



# def activate(request,uidb64,token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         myuser = User.objects.get(pk=uid)
#     except (TypeError,ValueError,OverflowError,User.DoesNotExist):
#         myuser = None

#     if myuser is not None and generate_token.check_token(myuser,token):
#         myuser.is_active = True
#         # user.profile.signup_confirmation = True
#         myuser.save()
#         login(request,myuser)
#         messages.success(request, "Your Account has been activated!!")
#         return redirect('signin')
#     else:
#         return render(request,'activation_failed.html')