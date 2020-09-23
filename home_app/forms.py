from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django import forms

from verification.models import Trial

from verification.models import DetailsOfApplication


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class AddTrial(forms.ModelForm):
    class Meta:
        model = Trial
        exclude = []
        widgets = {
            'date': DatePickerInput(),
            'time': TimePickerInput()
        }


class ApplicationDetails(forms.ModelForm):
    class Meta:
        model = DetailsOfApplication
        exclude = ['application']

