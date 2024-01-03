from django.db import models
from app_buyer.models import *

# Create your models here.

class Seller(models.Model):
    username=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    sellerprofile_pic = models.FileField(upload_to='images/',default="p2.jpeg")
    
    def __str__(self):
        return self.username
    
class Category(models.Model):
    cname=models.CharField(max_length=200)
    cdiscription=models.TextField(max_length=200)
    user=models.ForeignKey(Seller,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.cname

class Product(models.Model):
    pname=models.CharField(max_length=200)
    price=models.IntegerField()
    image=models.FileField(upload_to="product/")
    discription=models.TextField(max_length=500)    
    user=models.ForeignKey(Seller,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    
    def __str__(self):
        return self.pname