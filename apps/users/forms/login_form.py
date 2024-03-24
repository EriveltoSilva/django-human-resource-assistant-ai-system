from django import forms
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(
         label="Username", 
         required=True,
         widget=forms.TextInput(attrs={
              "placeholder":"Insira o seu username",
              'class':"form-control form-control-lg"
         })
    )
    
    password = forms.CharField(
         label="Senha", 
         required=True,
         widget=forms.PasswordInput(attrs={
              "placeholder":"Insira a sua senha",
              'class':"form-control form-control-lg"
         })
    )
        
