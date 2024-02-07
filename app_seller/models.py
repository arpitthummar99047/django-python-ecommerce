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
    cname=models.CharField(max_length=200, unique=True, help_text="Category name (case-insensitive)")
    cdescription=models.TextField(max_length=200, null=True, blank=True)
    user=models.ForeignKey(Seller,on_delete=models.CASCADE)
   
    class Meta:
        unique_together = ['cname', 'user']
         
    def save(self, *args, **kwargs):
        self.cname = self.cname.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.cname.lower()    

    
class Product(models.Model):
    pname=models.CharField(max_length=200)
    price=models.IntegerField()
    image=models.FileField(upload_to="product/")
    discription=models.TextField(max_length=500)    
    user=models.ForeignKey(Seller,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.pname
    
    @property
    def category_name(self):
        return self.category.cname