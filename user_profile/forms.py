from django import forms
from verification.models import user_achievements


class Achievement(forms.ModelForm):
    class Meta:
        model = user_achievements
        exclude = ['user']
