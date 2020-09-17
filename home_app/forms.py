from django import forms

from verification.models import Trial


class AddTrial(forms.ModelForm):
    class Meta:
        model = Trial
        exclude = (None,)
