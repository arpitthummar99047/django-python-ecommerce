from django.shortcuts import render
from app_seller.models import *
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
import random

# Create your views here.

def seller_index(request):
    return render(request,'seller_index.html')

def seller_home(request):
    context = {}
    seller_data=Seller.objects.get(email=request.session["email"])
    context["seller_data"]=seller_data
    return render(request,'seller_home.html',context)

def seller_signup(request):
    context = {}

    if request.method == "POST":
        try:
            user_exist = Seller.objects.get(email=request.POST["email"])
            context["msg"] = "User Already Exists"
        except:
            if request.POST["password"] == request.POST["confirmPassword"]:
                global seller_otp
                seller_otp = random.randint(100000, 999999)

                subject = 'OTP Verification code'
                message = f'Thanks for choosing us, your OTP is: {seller_otp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST["email"], ]

                send_mail(subject, message, email_from, recipient_list)

                global seller_data
                seller_data = {
                    "username": request.POST["username"], 
                    "email": request.POST["email"],
                    "password": request.POST["password"],
                }
                return render(request, "seller_otp.html")
            else:
                context["pass"] = "Passwords do not match"
    return render(request,'seller_signup.html')


def seller_otp(request):
    context = {}

    if request.method == "POST":
        if  seller_otp == int(request.POST["seller_otp"]):
            Seller.objects.create(
                username=seller_data["username"],
                email=seller_data["email"],
                password=make_password(seller_data["password"]),
            )
            context["msg"] = "Registration Successful"
            return render(request, "seller_login.html", context)
        else:
            context["msg"] = "Invalid OTP"
    return render(request,'seller_signup.html')


def seller_login(request):
    context = {}

    if request.method == "POST":
        try:
            current_user = Seller.objects.get(email=request.POST["email"])
            if check_password(request.POST["password"], current_user.password):
                context["msg"] = "Login Successful"
                request.session["email"]=request.POST["email"]
                seller_data=Seller.objects.get(email=request.session["email"])
                context["seller_data"]=seller_data
                return render(request, "seller_profile.html",context)
            else:
                context["msg"] = "Incorrect password"
        except:
            context["msg"] = "Invalid User"

    return render(request, "seller_login.html", context)

def seller_logout(request):
    context={}
    del request.session["email"]
    context["msg"]="Logout successfull"
    return render(request,"seller_login.html",context)


def seller_profile(request):
    context = {}
    seller_data=Seller.objects.get(email=request.session["email"])
    context["seller_data"]=seller_data
    if request.method=="POST":
        seller_data.username=request.POST["username"]
        seller_data.email=request.POST["email"]
       
        #password check
        if check_password(request.POST["opassword"],seller_data.password):
            if request.POST["npassword"]==request.POST["cnpassword"]:
                seller_data.password=make_password(request.POST["npassword"])
            else:
                context["seller_data"]="Password does Not Match"
        else:
            context["seller_data"]="Old Password Not Match"
            
        try:
            request.FILES["propic"]
            seller_data.sellerprofile_pic=request.FILES["propic"] 
        except:
            pass       
        seller_data.save()
        context["msg"]="Profile Updated Succefully"
            
    return render(request, "seller_profile.html",context)


def seller_addproduct(request, product_id=None):
    context = {}
    
    # Get the seller data based on the session email
    seller_data = Seller.objects.get(email=request.session["email"])
    context["seller_data"] = seller_data

    # Check if default categories already exist for the current user
    default_categories = ["Cloths", "Toys", "Home & Kitchen"]
    for category_name in default_categories:
        existing_category = Category.objects.filter(
            cname__iexact=category_name, user=seller_data
        ).first()
        if not existing_category:
            Category.objects.create(cname__iexact=category_name, user=seller_data)

    # Fetch all available categories
    all_categories = Category.objects.filter(user=seller_data)
    context["categories"] = all_categories

    if request.method == "POST":
        user_exists = Seller.objects.get(email=request.session["email"])
        # Convert category_id to an integer
        category_id = int(request.POST["category"])

        if category_id == 0:
            # User wants to add a new category
            new_category_name = request.POST.get("new_category_name").strip()
            # Check if a category with the same name already exists for the current seller
            existing_category = Category.objects.filter(
                cname__iexact=new_category_name, user=user_exists
            ).first()
            if existing_category:
                context["msg"] = "Category already exists."
                return render(request, "seller_addproduct.html", context)

            new_category_description = request.POST.get("new_category_description")

            # Create a new category and associate it with the current user
            new_category = Category.objects.create(
                cname=new_category_name,
                cdescription=new_category_description,
                user=user_exists
            )
            # Use the newly created category for the product
            category = new_category
        else:
            # User selected an existing category
            try:
                category = Category.objects.get(id=category_id, user=user_exists)
            except Category.DoesNotExist:
                # Handle the case where the selected category doesn't exist
                context["msg"] = "Selected category does not exist."
                return render(request, "seller_addproduct.html", context)

        # Check if product_id is provided for updating
        if product_id:
            # Update existing product
            product = Product.objects.get(id=product_id)
            product.pname = request.POST["pname"]
            product.price = request.POST["price"]
            product.image = request.FILES["productpic"]
            product.description = request.POST["desc"]
            product.category = category
            product.save()
            context["msg"] = "Product updated successfully"
        else:
            # Create new product
            Product.objects.create(
                pname=request.POST["pname"],
                price=request.POST["price"],
                image=request.FILES["productpic"],
                discription=request.POST["desc"],
                category=category,
                user=user_exists
            )
            context["msg"] = "Product added successfully"

    return render(request, "seller_addproduct.html", context)










        
            
        
        
    
    
    
    

