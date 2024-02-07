from django.shortcuts import render,redirect
from app_buyer.models import *
from app_seller.models import *
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from decimal import Decimal
import random

def index(request):
    context = {}
    all_product=Product.objects.all()
    context["all_product"]=all_product
    return render(request, "index.html",context)

def home(request):
    context = {}
    user_data=User.objects.get(email=request.session["email"])
    context["user_data"]=user_data
    all_product=Product.objects.all()
    context["all_product"]=all_product
    return render(request, "home.html",context)

def register(request):
    context = {}

    if request.method == "POST":
        try:
            user_exist = User.objects.get(email=request.POST["email"])
            context["emailerror"] = "User Already Exists,pls try to login"
            return render(request, "register.html", context)
            
        except User.DoesNotExist:
            try:
                # Check if username already exists
                user_exist_username = User.objects.get(username=request.POST["username"])
                context["usernameerror"] = "Username already exists, please choose a different one"
                return render(request, "register.html", context)
            except User.DoesNotExist:
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
            current_user = User.objects.get(email=request.POST["login_email"])
            if check_password(request.POST["login_password"], current_user.password):
                context["loginsucc"] = "Login Successfull"
                request.session["email"]=request.POST["login_email"]
                user_data=User.objects.get(email=request.session["email"])
                context["user_data"]=user_data
                return render(request, "index.html",context)
            else:
                context["incorectpass"] = "Incorrect password"
        except:
            context["invaliduser"] = "Invalid User"

    return render(request, "register.html", context)

def logout(request):
    context = {}

    # Check if the email is present in the session before deleting
    if "email" in request.session:
        del request.session["email"]
        context["msg"] = "Logout successful"
    else:
        context["msg"] = "You are not logged in"

    # Redirect to the login page after logout
    return redirect("index") 




def profile(request):
    context = {}
    user_data=User.objects.get(email=request.session["email"])
    context["user_data"]=user_data
    if request.method=="POST":
        user_data.username=request.POST["username"]
        # user_data.email=request.POST["email"]
       
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


def viwe_cart(request):
    context = {}
    user_data = User.objects.get(email=request.session["email"])
    context["user_data"] = user_data

    cart_product = Cart.objects.filter(user=user_data)
    
    # Calculate subtotal for each cart item
    total_quantity = 0
    for cart_item in cart_product:
        cart_item.subtotal = Decimal(cart_item.product.price) * cart_item.quantity
        total_quantity += cart_item.quantity
    
    # Calculate total based on cart item subtotals
    total = sum(cart_item.subtotal for cart_item in cart_product)
    context["cart_product"] = cart_product
    context["total"] = total
    context["total_quantity"] = total_quantity
    
    return render(request, "cart.html", context)


def pro_view(request, id):
    one_data = Product.objects.get(id=id)
    context = {
        'one_data': one_data,
    }
    return render(request, "pro_view.html", context) 


def chekout(request):
    context = {}
    user_data = User.objects.get(email=request.session["email"])
    context["user_data"] = user_data
    
    cart_product = Cart.objects.filter(user=user_data)
    
    # Calculate subtotal for each cart item
    total_quantity = 0
    for cart_item in cart_product:
        cart_item.subtotal = Decimal(cart_item.product.price) * cart_item.quantity
        total_quantity += cart_item.quantity
    
    # Calculate total based on cart item subtotals
    total = sum(cart_item.subtotal for cart_item in cart_product)
    context["cart_product"] = cart_product
    context["total"] = total
    context["total_quantity"] = total_quantity
    
    if request.method == "POST":
        global shipping_data
        shipping_data = {
            "first_name": request.POST["first_name"], 
            "last_name": request.POST["last_name"],
            "search_country": request.POST["search_country"],
            "order_address_line1": request.POST["order_address_line1"],
            "order_address_line2": request.POST["order_address_line2"],
            "order_city": request.POST["order_city"],
            "order_zipcode": request.POST["order_zipcode"],
            "order_phone": request.POST["order_phone"],
            "order_email": request.POST["order_email"],
            
        }
        
        # Create an instance of Orderdetail and save it
        order_detail_instance = Orderdetail.objects.create(
            first_name=shipping_data["first_name"],
            last_name=shipping_data["last_name"],
            search_country=shipping_data["search_country"],
            order_address_line1=shipping_data["order_address_line1"],
            order_address_line2=shipping_data["order_address_line2"],
            order_city=shipping_data["order_city"],
            order_zipcode=shipping_data["order_zipcode"],
            order_phone=shipping_data["order_phone"],
            order_email=shipping_data["order_email"],
        )
        order_detail_instance.save()
        
        context["msg"]="shipping address add"
        
        payment_method = request.POST.get('checkout_payment_method')

        if payment_method == 'online':
            # Logic for online payment
            context = {"msg": "online payment"}
            return render(request, 'confirmorder.html', {'payment_method': 'online'})
        elif payment_method == 'cash':
            # Logic for cash payment
            context = {"msg": "cash payment"}
            return render(request, 'confirmorder.html', {'payment_method': 'cash'})

    return render(request, "chekout.html", context)
   
    



def confirmorder(request):
    context = {}
    user_data = User.objects.get(email=request.session["email"])
    context["user_data"] = user_data
    
    cart_product = Cart.objects.filter(user=user_data)
    
    # Calculate subtotal for each cart item
    for cart_item in cart_product:
        cart_item.subtotal = Decimal(cart_item.product.price) * cart_item.quantity

    
    # Calculate total based on cart item subtotals
    total = sum(cart_item.subtotal for cart_item in cart_product)
    context["cart_product"] = cart_product
    context["total"] = total

  
    return render(request, "confirmorder.html", context)   


