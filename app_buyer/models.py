from django.db import models

# Create your models here.


class User(models.Model):
    username=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    profile_pic = models.FileField(upload_to='images/',default="p2.jpeg")
    
    def __str__(self):
        return self.username
