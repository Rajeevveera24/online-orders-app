from django.contrib import admin
from .models import Shop, Order, User_Type, Order_Item, Test_Model

admin.site.register(Order)
admin.site.register(Order_Item)
admin.site.register(User_Type)
admin.site.register(Shop)
admin.site.register(Test_Model)