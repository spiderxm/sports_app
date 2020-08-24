from django import forms

from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class Register(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'gender', 'age', 'state', 'sport']


class Login(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['email']
