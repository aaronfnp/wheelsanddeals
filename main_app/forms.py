from django import forms
from django.forms import ModelForm
from .models import Car, Review, Profile
from django.contrib.auth.models import User



class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ['published_by']

class CarForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['user_sender']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']