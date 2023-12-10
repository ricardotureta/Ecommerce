from django import forms
from django.contrib.auth.models import User
from .models import Customer

class LoginForms(forms.Form):
    username = forms.EmailField(label='Email')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    
class UserForms(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
    first_name = forms.CharField(label='Nome', )
    last_name = forms.CharField(label='Sobrenome', )
    username = forms.CharField(label='Usuario')
    email = forms.EmailField(label='Email', )
    password = forms.CharField(label='Senha', widget=forms.PasswordInput, )