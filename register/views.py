from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, authenticate
from orders.models import Shop, Order

# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            
            form.save()
            
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            
            user = authenticate(username=username, password=raw_password)
            login(response, user)
            
            shop = Shop(name = "Shop_" +str(user.username), address = "", user = user)
            shop.save()
            
            order = Order(user = user)
            order.save()

            return redirect('home')
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form":form})