from django.contrib import admin
from app_buyer.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Cart)
admin.site.register(Orderdetail)