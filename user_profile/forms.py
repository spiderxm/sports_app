from django import forms


class Form(forms.Form):
    image = forms.ImageField()