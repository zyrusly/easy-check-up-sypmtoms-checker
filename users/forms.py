from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model= User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    location = forms.CharField(max_length=225)
    class Meta:
        model= Profile
        fields = ['image','location']