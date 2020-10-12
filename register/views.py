from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from django.contrib.auth import login, authenticate
from orders.models import Shop, Order, User_Type
from django.http import HttpResponse

# Create your views here.
def register(response):
    if response.user.is_authenticated:
        # return HttpResponse("Hello")
        user_type = get_object_or_404(User_Type, user = response.user)
        # return HttpResponse("Hell")
        if user_type.privilege == True:
            # return HttpResponse("Hey!!") -- works till here
            if response.method == "POST":
                form = RegisterForm(response.POST)
                if form.is_valid():    
                    form.save()
                    username = form.cleaned_data.get('username')
                    raw_password = form.cleaned_data.get('password1')
                    user = authenticate(username = username, password = raw_password)
                    # login(response, user) - DON'T log in newly created, since this would log out privileged user 
                    shop = Shop(name = "Shop_" +str(user.username), address = "", user = user)
                    shop.save()
                    user_type = User_Type(privilege = False, user = user)
                    user_type.save()

                    return redirect('/register/')       # Return a fresh form to register another user
            else:
                form = RegisterForm()
            return render(response, "register/register.html", {"form":form, "privilege": True})
        else:
            # return HttpResponse("Hellllo!")
            return redirect("/home") # if user is logged in, but does not have privilege to access this page, send them to home
    else:
        return redirect("/login")   # if user is not logged in, redirect to login page