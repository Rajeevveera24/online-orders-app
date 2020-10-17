import os
from django.contrib import admin
from django.urls import path, include
from register import views as v_reg

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('orders.urls'), name = "order"),
    path('', include('django.contrib.auth.urls')),
    path('item/', include('item.urls')),
    path('register/', v_reg.register, name = 'register'),
    path('accounts/', include('django.contrib.auth.urls')),
]
