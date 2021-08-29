from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin as LRM
from django.urls import reverse_lazy, reverse

from .models import Item
from orders.models import User_Type
from .forms import CreateItemForm


class ItemCreateView(LRM, View):
    template_name = "item/item_create_form.html"
    success_url = "/item/view/"

    def get(self, response):
        priv = get_object_or_404(User_Type, user=response.user)
        if priv == False:
            return redirect("/logout/")
        form = CreateItemForm()
        ctx = {"form": form, "privilege": priv}
        return render(response, self.template_name, ctx)

    def post(self, response):
        priv = get_object_or_404(User_Type, user=response.user)
        if priv == False:
            return redirect("/logout/")

        form = CreateItemForm(response.POST)

        if not form.is_valid():
            ctx = {"form": form, "privilege": priv}
            return render(response, self.template_name, ctx)

        form.save()

        return redirect(self.success_url)


class ItemListView(LRM, ListView):
    model = Item
    template_name = "item/item_list_form.html"

    def get(self, response):
        priv = get_object_or_404(User_Type, user=response.user).privilege

        if priv == False:
            return redirect("/logout/")

        items = Item.objects.all().order_by("id")

        ctx = {"privilege": priv, "item_list": items}

        return render(response, self.template_name, ctx)


class ItemUpdateView(LRM, View):
    template_name = "item/item_create_form.html"
    success_url = "/item/view/"

    def get(self, response, pk):
        priv = get_object_or_404(User_Type, user=response.user).privilege
        if priv == False:
            return redirect("/logout/")

        item = get_object_or_404(Item, id=pk)
        form = CreateItemForm(instance=item)
        ctx = {"form": form, "privilege": priv}
        return render(response, self.template_name, ctx)

    def post(self, response, pk=None):
        priv = get_object_or_404(User_Type, user=response.user).privilege
        if priv == False:
            return redirect("/logout/")

        item = get_object_or_404(Item, id=pk)
        form = CreateItemForm(response.POST, instance=item)

        if not form.is_valid():
            ctx = {"form": form, "privilege": priv}
            return render(response, self.template_name, ctx)

        item = form.save()
        item.save()

        return redirect(self.success_url)


class ItemDeleteView(LRM, DeleteView):
    model = Item
    template_name = "item/item_delete_view.html"
    success_url = "/item/view"
