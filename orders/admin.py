from django.contrib import admin
from .models import Shop, Order, User_Type, Item

admin.site.register(Shop)
admin.site.register(Order)
admin.site.register(User_Type)
admin.site.register(Item)