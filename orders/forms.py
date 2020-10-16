from django import forms
from .models import Shop, Order, Item

class CreateShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['address', 'name']

class CreateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
