from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ['published_by']