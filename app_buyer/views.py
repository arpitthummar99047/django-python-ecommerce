from django.shortcuts import render,redirect
from app_buyer.models import *
from app_seller.models import *
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
import random

def index(request):
    context = {}
    all_product=Product.objects.all()
    context["all_product"]=all_product
    return render(request, "index.html",context)

def register(request):
    context = {}

    if request.method == "POST":
        try:
            user_exist = User.objects.get(email=request.POST["email"])
            context["msg"] = "User Already Exists,pls try to login"
            
        except:
            if request.POST["password"] == request.POST["confirmPassword"]:
                global otp
                otp = random.randint(100000, 999999)

                subject = 'OTP Verification code'
                message = f'Thanks for choosing us, your OTP is: {otp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST["email"], ]

                send_mail(subject, message, email_from, recipient_list)

                global user_data
                user_data = {
                    "username": request.POST["username"], 
                    "email": request.POST["email"],
                    "password": request.POST["password"],
                }
                return render(request, "otp.html")
            else:
                context["pass"] = "Passwords do not match"

    return render(request, "register.html", context)

def otp(request):
    context = {}

    if request.method == "POST":
        if otp == int(request.POST["otp"]):
            User.objects.create(
                username=user_data["username"],
                email=user_data["email"],
                password=make_password(user_data["password"]),
            )
            context["msg"] = "Registration Successful"
            return render(request,"login.html",context)
        else:
            context["msg"] = "Invalid OTP"

    return render(request, "register.html", context)

def login(request):
    context = {}

    if request.method == "POST":
        try:
            current_user = User.objects.get(email=request.POST["email"])
            if check_password(request.POST["password"], current_user.password):
                context["msg"] = "Login Successfull"
                request.session["email"]=request.POST["email"]
                user_data=User.objects.get(email=request.session["email"])
                context["user_data"]=user_data
                return render(request, "index.html",context)
            else:
                context["msg"] = "Incorrect password"
        except:
            context["msg"] = "Invalid User"

    return render(request, "login.html", context)

def logout(request):
    context={}
    del request.session["email"]
    context["msg"]="Logout successfull"
    return render(request,"login.html",context)

def home(request):
    context = {}
    user_data=User.objects.get(email=request.session["email"])
    context["user_data"]=user_data
    return render(request, "home.html",context)



def profile(request):
    context = {}
    user_data=User.objects.get(email=request.session["email"])
    context["user_data"]=user_data
    if request.method=="POST":
        user_data.username=request.POST["username"]
        user_data.email=request.POST["email"]
       
        #password check
        if check_password(request.POST["opassword"],user_data.password):
            if request.POST["npassword"]==request.POST["cnpassword"]:
                user_data.password=make_password(request.POST["npassword"])
            else:
                context["user_data"]="Password does Not Match"
        else:
            context["user_data"]="Old Password Not Match"
            
        try:
            request.FILES["propic"]
            user_data.profile_pic=request.FILES["propic"] 
        except:
            pass       
        user_data.save()
        context["msg"]="Profile Updated Succefully"
            
    return render(request, "profile.html",context)
            

def shophome(request):
    context = {}
    user_data=User.objects.get(email=request.session["email"])
    context["user_data"]=user_data
    all_product=Product.objects.all()
    context["all_product"]=all_product
    return render(request, "shophome.html",context)

def shopindex(request):
    context = {}
    all_product=Product.objects.all()
    context["all_product"]=all_product
    return render(request, "shopindex.html",context)
    

def cart(request,id):
    current_product=Product.objects.get(id=id)
    current_user=User.objects.get(email=request.session["email"])
    cart_exists=Cart.objects.filter(product=current_product,user=current_user)
    # print(cart_exists)
    if cart_exists:
        cart_exists[0].quantity+=1
        cart_exists[0].save()
    else:
        Cart.objects.create(
        product=current_product,
        user=current_user
        )
    return redirect("shophome")