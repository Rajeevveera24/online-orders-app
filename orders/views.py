from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Shop
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin as LRM
from django.urls import reverse_lazy, reverse
from .forms import CreateShopForm, CreateOrderForm

def home(response):
	return render(response, "orders/home.html", {})

def view(response):
    if response.user.is_authenticated:
        return render(response, "orders/view.html", {})
    else:
        return redirect("/login")

class ShopUpdateView(LRM, View):
    template_name = 'orders/shopupdate_form.html'
    success_url = reverse_lazy('home')

    def get(self, request):
        shop = get_object_or_404(Shop, user = self.request.user)
        form = CreateShopForm(instance = shop)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        shop = get_object_or_404(Shop, user = self.request.user)
        form = CreateShopForm(request.POST, instance = shop)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        
        shop.save()

        return redirect(self.success_url)

# class OrderCreateView(LRM, View):
#     template_name = 'orders/ordercreate_form.html'
#     success_url = reverse_lazy('view')

#     def get(self, request):
#         form = CreateOrderForm()
#         ctx = {'form': form}
#         return render(request, self.template_name, ctx)

#     def post(self, request):
#         form = CreateOrderForm(request.POST)

#         if not form.is_valid():
#             ctx = {'form': form}
#             return render(request, self.template_name, ctx)

#         order = form.save(commit = False)
#         order.user = request.user
#         order.save(commit = True)

#         return redirect(self.success_url)

class OrderUpdateView(LRM, View):
    template_name = 'orders/orderupdate_form.html'
    success_url = reverse_lazy('view')

    def get(self, request):
        order = get_object_or_404(Order, user = self.request.user)
        form = CreateOrderForm(instance = order)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        order = get_object_or_404(Order, user = self.request.user)
        form = CreateOrderForm(request.POST, instance = order)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        
        order.save()

        return redirect(self.success_url)