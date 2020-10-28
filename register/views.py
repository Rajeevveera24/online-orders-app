from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin as LRM

from .forms import RegisterForm
from orders.models import Shop, Order, User_Type

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

class UserListView(LRM, View):
    model = User
    template_name = "register/user_list.html"

    def get(self, response):
        user_type = get_object_or_404(User_Type, user = response.user)
        priv = user_type.privilege
        if priv == True:
            users = User.objects.all().order_by('id')
        else:
            return redirect('/logout')

        ctx = {'privilege' : priv, 'user_list' : users}

        return render(response, self.template_name, ctx)

class UserUpdateView(LRM, View):
    template_name = 'register/user_update_form.html'
    success_url = '/register/view/'

    def get(self, response, pk):
        priv = get_object_or_404(User_Type, user = response.user).privilege
        if priv == False:
            return redirect("/logout/")

        user = get_object_or_404(User, id = pk)
        form = RegisterForm(instance = user)
        ctx = {'form': form, 'privilege': priv, 'u':user}
        return render(response, self.template_name, ctx)

    def post(self, response, pk = None):
        priv = get_object_or_404(User_Type, user = response.user).privilege
        if priv == False:
            return redirect("/logout/")
        
        try:
            user = get_object_or_404(User, id = pk)
        except:
            return response("User does not exist. Go back and Create new user instead.")

        form = RegisterForm(response.POST, instance = user)

        if not form.is_valid():
            ctx = {'form': form, 'privilege': priv, 'u':user}
            return render(response, self.template_name, ctx)

        user = form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username = username, password = raw_password)

        return redirect(self.success_url)

class UserDeleteView(LRM, View):
    template_name = 'register/user_delete_form.html'
    success_url = '/register/'

    def get(self, response, pk = None):
        user_item = get_object_or_404(User_Type, user = response.user)
        priv = user_item.privilege
        user = get_object_or_404(User, id = pk)

        if priv == True:
            return render(response, self.template_name, {'u':user, 'privilege': priv})
        
        return HttpResponse("You don't have permission to delete this user\nYou can go back to a previous page or contact the website administrators if you think this is a mistake")

    def post(self, response, pk = None):
        user_item = get_object_or_404(User_Type, user = response.user)
        priv = user_item.privilege

        user = get_object_or_404(User, id = pk)

        if priv == True:
            user.delete()
            return redirect(self.success_url)
        
        return HttpResponse("You don't have permission to delete this order\nYou can go back to a previous page or contact the website administrators if you think this is a mistake")
        