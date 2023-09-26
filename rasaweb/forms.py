from django import forms
from .models import User, Messege


class RegisterForm(forms.ModelForm):
    passwrd = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['name', 'email', 'passwrd', 'age']

class MassageForm(forms.ModelForm):
    passwrd = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Messege
        fields = ['messege']
