from django.contrib import admin
from .models import Shop, Order, User_Type, Item, Order_Item

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Order_Item)
admin.site.register(User_Type)
admin.site.register(Shop)