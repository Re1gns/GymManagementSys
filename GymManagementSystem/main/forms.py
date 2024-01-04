from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget
from . import models

class EnquiryForm(forms.ModelForm):
    class Meta:
        model= models.Enquiry
        widgets = {
            'content': CKEditorWidget(),
        }
        fields=('full_name', 'email', 'phone_number', 'details')

class Signup(UserCreationForm):
    class Meta:
        model = User
        widgets = {
            'content': CKEditorWidget(),
        }
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class EditProfile(UserChangeForm):
    class Meta:
        model=User
        widgets = {
            'content': CKEditorWidget(),
        }
        fields=('first_name', 'last_name', 'username', 'email')

class TrainerLogin(forms.ModelForm):
    class Meta:
        model=models.Trainer
        widgets = {
            'content': CKEditorWidget(),
        }
        fields = ('username', 'pwd')

class TrainerProfile(forms.ModelForm):
    class Meta:
        model=models.Trainer
        widgets = {
            'content': CKEditorWidget(),
        }
        fields = ('Full_Name', 'pwd', 'tel', 'Home_Address', 'Email', 'details', 'profile_picture')

class TrainerChangePassword(forms.Form):
    new_password=forms.CharField(max_length=50, required=True)

class ReportATrainerForm(forms.ModelForm):
    class Meta:
        model=models.TrainerSubscriberReport
        fields = ('report_a_trainer', 'report_msg', 'reporting_user')
        widgets = {'content': CKEditorWidget(), 'reporting_user': forms.HiddenInput()}

class ReportAUserForm(forms.ModelForm):
    class Meta:
        model=models.TrainerSubscriberReport
        fields = ('report_a_user', 'report_msg', 'reporting_trainer')
        widgets = {'content': CKEditorWidget(), 'reporting_trainer': forms.HiddenInput()}

