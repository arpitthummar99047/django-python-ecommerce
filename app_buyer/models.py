from django.db import models
from app_seller.models import Product

# Create your models here.


class User(models.Model):
    username=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    profile_pic = models.FileField(upload_to='images/',default="p2.jpeg")
    
    def __str__(self):
        return self.username
    

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product", related_name="cart_items")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User", related_name="cart_items")
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return "{} - {}".format(self.product.pname, self.quantity)   
    
