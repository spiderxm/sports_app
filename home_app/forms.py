from django import forms

from verification.models import Trial


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class AddTrial(forms.ModelForm):
    class Meta:
        model = Trial
        exclude = []
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'time': TimeInput(attrs={'type': 'time'}),
        }
