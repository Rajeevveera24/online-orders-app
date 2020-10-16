from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Shop, User_Type, Item, Order_Item
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin as LRM
from django.urls import reverse_lazy, reverse
from .forms import CreateShopForm, CreateItemForm

def home(response):
    priv = False
    if response.user.is_authenticated:
        priv = get_object_or_404(User_Type, user = response.user).privilege
    return render(response, "orders/home.html", {'privilege': priv})

class OrderListView(LRM, View):
    model = Order
    template_name = "orders/order_list.html"

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
    template_name = 'orders/order_create.html'
    success_url = "/view/order/"

    def get(self, response):
        ctx = dict()
        items = Item.objects.all()
        ctx["items"] = items
        ctx["privilege"] = get_object_or_404(User_Type, user = response.user).privilege
        
        return render(response, self.template_name, ctx)

    def post(self, response):
        # print(response.POST)
        # print(type(response.POST))
        items = Item.objects.all()
        order = Order(user = response.user)
        products = {}
        form_input = response.POST

        # print(form_input)

        for it in items:
            if int(form_input.get(str(it))) > 0:
                products[it] = int(form_input.get(str(it)))
        
        if products == {}:
            return redirect("/create/")
        
        try:
            order.save()
            for p,q in products.items():
                order_item = Order_Item(order = order, item = p, qty = int(q))
                order_item.save()
        except Exception as e:
            print(str(e))
            order.delete()
            return HttpResponse("Unable to process your order. Please go back to the previous page and order again")
        
        return redirect(self.success_url + str(order.id))

# class OrderUpdateView(LRM, View):
#     template_name = 'orders/orderupdate_form.html'
#     success_url = reverse_lazy('view')

#     def get(self, response):
#         order = get_object_or_404(Order, user = response.user)
#         form = CreateOrderForm(instance = order)
#         ctx = {'form': form}
#         user_type = get_object_or_404(User_Type, user = response.user)
#         # ctx = dict()
#         ctx['privilege'] = user_type.privilege
#         return render(response, self.template_name, ctx)

#     def post(self, response):
#         order = get_object_or_404(Order, user = response.user)
#         form = CreateOrderForm(response.POST, instance = order)

#         if not form.is_valid():
#             ctx = {'form': form}
#             return render(response, self.template_name, ctx)
        
#         order.save()

#         return redirect(self.success_url)

class ItemCreateView(LRM, View):
    template_name = 'orders/item_create_form.html'
    success_url = reverse_lazy('item_view')

    def get(self, response):
        priv = get_object_or_404(User_Type, user = response.user)
        if priv == False:
            return redirect('/logout/')
        form = CreateItemForm()
        ctx = {'form': form, 'privilege':priv}
        return render(response, self.template_name, ctx)

    def post(self, response):
        priv = get_object_or_404(User_Type, user = response.user)
        if priv == False:
            return redirect('/logout/')

        form = CreateItemForm(response.POST)
        
        if not form.is_valid():
            ctx = {'form': form, 'privilege': priv}
            return render(response, self.template_name, ctx)

        form.save()

        return redirect(self.success_url)

class ItemListView(LRM, View):
    model = Item
    template_name = "orders/item_list_form.html"

    def get(self, response):
        priv = get_object_or_404(User_Type, user = response.user).privilege

        if priv == False:
            return redirect("/logout/")
        
        items = Item.objects.all()

        ctx = {'privilege' : priv, 'item_list' : items}

        return render(response, self.template_name, ctx)

# class ShopUpdateView(LRM, View):
#     template_name = 'orders/shopupdate_form.html'
#     success_url = reverse_lazy('home')

#     def get(self, response):
#         shop = get_object_or_404(Shop, user = self.response.user)
#         form = CreateShopForm(instance = shop)
#         ctx = {'form': form}
#         return render(response, self.template_name, ctx)

#     def post(self, response):
#         shop = get_object_or_404(Shop, user = self.response.user)
#         form = CreateShopForm(response.POST, instance = shop)

#         if not form.is_valid():
#             ctx = {'form': form}
#             return render(response, self.template_name, ctx)
        
#         shop.save()

#         return redirect(self.success_url)

# def view(response):
#     if response.user.is_authenticated:
#         user_type = get_object_or_404(User_Type, user = response.user)
#         ctx = dict()
#         ctx['privilege' ] = user_type.privilege
#         return render(response, "orders/view.html", ctx)
#     else:
#         return redirect("/login")