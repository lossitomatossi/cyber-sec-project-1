from django import forms
from .models import User
from django.db import connection

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Check if passwords match
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class PetSearch(forms.Form):
    owner_id = forms.CharField(widget=forms.TextInput, label="owner_id")