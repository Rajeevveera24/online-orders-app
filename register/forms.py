from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    # email = forms.EmailField()
    # shop_name = forms.CharField(max_length = 200)

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
