from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin as LRM
from django.urls import reverse_lazy, reverse

from .models import Order, Order_Item, Shop, User_Type
from item.models import Item
from .forms import CreateShopForm
import datetime as dt

def home(response):
    # priv = False
    # if response.user.is_authenticated:
    #     priv = get_object_or_404(User_Type, user = response.user).privilege
    # return render(response, "orders/home.html", {'privilege': priv})
    return redirect("/login")

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

        for ord in orders:
            ord.updated = ord.updated_at.strftime("%d-%m-%Y @ %H:%M")

        ctx = {'privilege' : priv, 'order_list' : orders}

        return render(response, self.template_name, ctx)

class OrderDetailView(LRM, View):
    model = Order
    template_name = "orders/order_detail.html"
    def get(self, response, pk):
        user_type = get_object_or_404(User_Type, user = response.user)
        priv = user_type.privilege
        order = Order.objects.get(id = pk)
        order.updated = order.updated_at.strftime("%d-%m-%Y @ %H:%M")
        items = Order_Item.objects.filter(order = order)
        context = {'order': order, 'privilege': priv, 'items':items, 'is_deleteable': False}
        
        cur_time = dt.datetime.now()
        cur_hour = int(cur_time.strftime("%H"))

        if cur_hour < 6 or cur_hour >= 18:
            created_time = order.created_at
            diff = cur_time - created_time
            if diff.seconds <= 43200 or priv == True: #users can delete orders upto 12 hours after placing them...
                context['is_deleteable'] = True

        return render(response, self.template_name, context)

class OrderCreateView(LRM, View):
    template_name = 'orders/order_create.html'
    wrong_time_page = 'orders/wrong_time.html'
    success_url = "/view/order/"

    def get(self, response):
        
        ctx = dict()
        ctx["privilege"] = get_object_or_404(User_Type, user = response.user).privilege
        
        cur_time = dt.datetime.now()
        cur_hour = int(cur_time.strftime("%H"))
        
        if cur_hour >= 6 and cur_hour < 18:    
            ctx["message"] = "Order can only be placed between 6:00 pm to 6:00 am the next day"
            return render(response, self.wrong_time_page, ctx)

        items = Item.objects.all()
        ctx["items"] = items
        
        return render(response, self.template_name, ctx)

    def post(self, response):

        cur_time = dt.datetime.now()
        cur_hour = int(cur_time.strftime("%H"))

        if cur_hour >= 6 and cur_hour < 18:    
            ctx = dict()
            ctx["privilege"] = get_object_or_404(User_Type, user = response.user).privilege
            ctx["message"] = "Order can only be placed between 6:00 pm to 6:00 am the next day"
            return render(response, self.wrong_time_page, ctx)


        items = Item.objects.all()
        order = Order(user = response.user)
        products = {}
        form_input = response.POST

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

class OrderDeleteView(LRM, View):
    template_name = 'orders/order_delete.html'
    wrong_time_page = 'orders/wrong_time.html'
    success_url = "/view/"

    def get(self, response, pk = None):
        user_item = get_object_or_404(User_Type, user = response.user)
        priv = user_item.privilege
        order = get_object_or_404(Order, id = pk)

        if priv == True:    #the admin can delete any order at any time
            return render(response, self.template_name, {'order':order, 'privilege': priv})         
        else:
            if order.user == response.user: #extra check to make sure that current user owns the order
                cur_time = dt.datetime.now()
                cur_hour = int(cur_time.strftime("%H"))
                
                if cur_hour >= 6 and cur_hour < 18:    
                    ctx = dict()
                    ctx["privilege"] = False
                    ctx["message"] = "Order can only be deleted between 6:00 pm to 6:00 am the next day"
                    return render(response, self.wrong_time_page, ctx)
                else:
                    created_time = order.created_at
                    diff = cur_time - created_time
                    if diff.seconds <= 43200: #users can delete orders upto 12 hours after placing them...
                        return render(response, self.template_name, {'order':order, 'privilege': priv})
                    else:
                        ctx = dict()
                        ctx["privilege"] = False
                        ctx["message"] = "Order cannot be deleted 12+ hours after it has been placed"
                        return render(response, self.wrong_time_page, ctx)
            else:
                return HttpResponse("You don't have permission to delete this order\nYou can go back to a previous page or contact the shop owners if you think this is an error")
        
        # if cur_hour >= 6 and cur_hour < 18:    
        #     ctx["message"] = "Order can only be placed between 6:00 pm to 6:00 am the next day"
        #     return render(response, self.wrong_time_page, ctx)

        # if priv == True or order.user == response.user:
        #     return render(response, self.template_name, {'order':order, 'privilege': priv})

    def post(self, response, pk = None):
        user_item = get_object_or_404(User_Type, user = response.user)
        priv = user_item.privilege
        order = get_object_or_404(Order, id = pk)

        if priv == True:    #admin can delete any order at any time
            order.delete()
            return redirect(self.success_url)
        else:
            if order.user == response.user: #extra check to make sure that current user owns the order
                cur_time = dt.datetime.now()
                cur_hour = int(cur_time.strftime("%H"))
                
                if cur_hour >= 6 and cur_hour < 18:    
                    ctx = dict()
                    ctx["privilege"] = False
                    ctx["message"] = "Order can only be deleted between 6:00 pm to 6:00 am the next day"
                    return render(response, self.wrong_time_page, ctx)
                else:
                    created_time = order.created_at
                    diff = cur_time - created_time
                    if diff.seconds <= 43200: #users can delete orders upto 12 hours after placing them...
                        order.delete()
                        return redirect(self.success_url)
                    else:
                        ctx = dict()
                        ctx["privilege"] = False
                        ctx["message"] = "Order cannot be deleted 12+ hours after it has been placed"
                        return render(response, self.wrong_time_page, ctx)
            else:
                return HttpResponse("You don't have permission to delete this order\nYou can go back to a previous page or contact the shop owners if you think this is an error")

        return HttpResponse("You don't have permission to delete this order\nYou can go back to a previous page or contact the shop owners if you think this is an error")
        
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