from django import forms
from verification.models import user_achievements
from bootstrap_datepicker_plus import DatePickerInput


class DateInput(forms.DateInput):
    input_type = 'date'


class Achievement(forms.ModelForm):
    class Meta:
        model = user_achievements
        exclude = ['user']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }
