from django import forms
from django.forms import ModelForm
from .models import Car, Review

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ['published_by']

class CarForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['user_sender']