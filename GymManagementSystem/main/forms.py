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

class TrainerProfile(forms.ModelForm):
    class Meta:
        model=models.Trainer
        fields = ('Full_Name', 'pwd', 'tel', 'Home_Address', 'Email', 'details', 'img')

class TrainerChangePassword(forms.Form):
    new_password=forms.CharField(max_length=50, required=True)

class ReportATrainerForm(forms.ModelForm):
    class Meta:
        model=models.TrainerSubscriberReport
        fields = ('report_a_trainer', 'report_msg', 'reporting_user')
        widgets = {'reporting_user': forms.HiddenInput()}

class ReportAUserForm(forms.ModelForm):
    class Meta:
        model=models.TrainerSubscriberReport
        fields = ('report_a_user', 'report_msg', 'reporting_trainer')
        widgets = {'reporting_trainer': forms.HiddenInput()}

