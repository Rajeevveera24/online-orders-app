import os
from django.contrib import admin
from django.urls import path, include
# from django.conf import settings
# from django.views.static import serve
from register import views as v_reg

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('orders.urls'), name = "order"),
    path("register/", v_reg.register, name = "register"),
    path('', include("django.contrib.auth.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
]
