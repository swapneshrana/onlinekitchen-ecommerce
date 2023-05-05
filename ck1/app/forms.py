from django.forms.fields import CharField
from django.db.models import fields
from django.db import models
from django.contrib.auth.models import User
import django
from django import forms 
from django.contrib.auth.forms import PasswordChangeForm
from .models import Address,Review


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['locality', 'city', 'state' ]
        widgets = {'locality':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Popular Place like Restaurant, Religious Site, etc.'}), 'city':forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}),
                    'state':forms.TextInput(attrs={'class':'form-control', 'placeholder':'State or Province'})}

class MychangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="old password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True, 'class':'form-control'}),
    )
    new_password1 = forms.CharField(
        label="New password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control'}),
    )
    new_password2 = forms.CharField(
        label="New password Again",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control'}),
    )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['subject','comment', 'rate']

     

