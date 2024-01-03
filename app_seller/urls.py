from django.urls import path
from app_seller import views

urlpatterns = [
   path('', views.seller_index, name='seller_index'),
   path('seller_home/', views.seller_home, name='seller_home'),
   path('seller_signup/',views.seller_signup, name="seller_signup"),
   path('seller_otp/',views.seller_otp,name='seller_otp'),
   path('seller_login/',views.seller_login,name='seller_login'),
   path('seller_profile/',views.seller_profile,name='seller_profile'),
   path('seller_logout/',views.seller_logout,name='seller_logout'),
   path('seller_addproduct/',views.seller_addproduct,name='seller_addproduct'),
  
  ]
