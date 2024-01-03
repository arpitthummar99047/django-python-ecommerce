from django.urls import path
from app_buyer import views

urlpatterns = [
   path('', views.index, name='index'),
   path('home/', views.home, name='home'),
   path('login/', views.login,name='login'),
   path('logout/',views.logout,name='logout'),
   path('register/',views.register,name='register'),
   path('shophome/',views.shophome,name='shophome'),
   path('shopindex/',views.shopindex,name='shopindex'),
   path('cart/',views.cart,name='cart'),
   path('otp/',views.otp,name='otp'),
   path('profile/',views.profile,name='profile'),
]
