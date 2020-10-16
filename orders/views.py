from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Shop, User_Type, Item, Order_Item
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin as LRM
from django.urls import reverse_lazy, reverse
from .forms import CreateShopForm, CreateOrderForm

def home(response):
    priv = False
    if response.user.is_authenticated:
        priv = get_object_or_404(User_Type, user = response.user).privilege
    return render(response, "orders/home.html", {'privilege': priv})

def view(response):
    if response.user.is_authenticated:
        user_type = get_object_or_404(User_Type, user = response.user)
        ctx = dict()
        ctx['privilege' ] = user_type.privilege
        return render(response, "orders/view.html", ctx)
    else:
        return redirect("/login")

class ShopUpdateView(LRM, View):
    template_name = 'orders/shopupdate_form.html'
    success_url = reverse_lazy('home')

    def get(self, response):
        shop = get_object_or_404(Shop, user = self.response.user)
        form = CreateShopForm(instance = shop)
        ctx = {'form': form}
        return render(response, self.template_name, ctx)

    def post(self, response):
        shop = get_object_or_404(Shop, user = self.response.user)
        form = CreateShopForm(response.POST, instance = shop)

        if not form.is_valid():
            ctx = {'form': form}
            return render(response, self.template_name, ctx)
        
        shop.save()

        return redirect(self.success_url)

class OrderListView(LRM, View):
    model = Order
    template_name = "orders/view.html"

    def get(self, response):
        user_type = get_object_or_404(User_Type, user = response.user)
        priv = user_type.privilege
        if priv == True:
            orders = Order.objects.all().order_by('-updated_at')
        else:
            orders = Order.objects.filter(user = response.user).order_by('-updated_at')

        ctx = {'privilege' : priv, 'order_list' : orders}

        return render(response, self.template_name, ctx)

class OrderDetailView(LRM, View):
    model = Order
    template_name = "orders/order_detail.html"
    def get(self, response, pk):
        user_type = get_object_or_404(User_Type, user = response.user)
        priv = user_type.privilege
        order = Order.objects.get(id = pk)
        items = Order_Item.objects.filter(order = order)
        context = { 'order': order, 'privilege': priv, 'items':items}
        
        return render(response, self.template_name, context)

class OrderCreateView(LRM, View):
    template_name = 'orders/ordercreate_form.html'
    success_url = reverse_lazy('view')

    def get(self, response):
        form = CreateOrderForm()
        ctx = {'form': form}
        return render(response, self.template_name, ctx)

    def post(self, response):
        form = CreateOrderForm(response.POST)

        if not form.is_valid():
            ctx = {'form': form}
            return render(response, self.template_name, ctx)

        order = form.save(commit = False)
        order.user = response.user
        order.save(commit = True)

        return redirect(self.success_url)

class OrderUpdateView(LRM, View):
    template_name = 'orders/orderupdate_form.html'
    success_url = reverse_lazy('view')

    def get(self, response):
        order = get_object_or_404(Order, user = response.user)
        form = CreateOrderForm(instance = order)
        ctx = {'form': form}
        user_type = get_object_or_404(User_Type, user = response.user)
        # ctx = dict()
        ctx['privilege'] = user_type.privilege
        return render(response, self.template_name, ctx)

    def post(self, response):
        order = get_object_or_404(Order, user = response.user)
        form = CreateOrderForm(response.POST, instance = order)

        if not form.is_valid():
            ctx = {'form': form}
            return render(response, self.template_name, ctx)
        
        order.save()

        return redirect(self.success_url)