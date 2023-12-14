from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from . import models

class EnquiryForm(forms.ModelForm):
    class Meta:
        model= models.Enquiry
        fields=('full_name', 'email', 'phone_number', 'details')

class Signup(UserCreationForm):
    class Meta:
        model=User
        fields=('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

class EditProfile(UserChangeForm):
    class Meta:
        model=User
        fields=('first_name', 'last_name', 'username', 'email')

class TrainerLogin(forms.ModelForm):
    class Meta:
        model=models.Trainer
        fields = ('username', 'pwd')