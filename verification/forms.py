from django import forms

from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class Register(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['email', 'age', 'state', 'sport']
