from django import forms
from .models import Shop, Order


class CreateShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ["address", "name"]
