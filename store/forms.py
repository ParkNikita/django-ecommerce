from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", 'email')
        field_classes = {"username": UsernameField}


class DeliveryCreationForm(forms.ModelForm):
    class Meta:
        model = models.DeliveryAddress
        fields = ('name', 'email', 'address', 'city', 'country', 'zip_code')

