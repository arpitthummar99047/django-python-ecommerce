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
   path('cart/<int:id>',views.cart,name='cart'),
   path('viwe_cart/',views.viwe_cart,name='viwe_cart'),
   path('pro_view/<int:id>',views.pro_view,name='pro_view'),
   path('otp/',views.otp,name='otp'),
   path('profile/',views.profile,name='profile'),
   path('chekout/',views.chekout,name='chekout'),
   path('confirmorder/',views.confirmorder,name='confirmorder'),

]
