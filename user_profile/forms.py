import datetime
from django import forms
from verification.models import user_achievements
from verification.models import Certificates


class DateInput(forms.DateInput):
    input_type = 'date'


class Achievement(forms.ModelForm):

    def clean(self):
        date = self.cleaned_data['date']
        if date > datetime.date.today():
            raise forms.ValidationError("The date cannot be in future!")

    class Meta:
        model = user_achievements
        exclude = ['user']
        widgets = {
            'date': DateInput(attrs={'type': 'date'})
        }

class Certificate(forms.ModelForm):
    class Meta:
        model = Certificates
        exclude = ['user']
