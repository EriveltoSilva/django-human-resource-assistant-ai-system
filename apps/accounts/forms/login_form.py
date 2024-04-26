from django import forms
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    email = forms.CharField(
         label="E-mail", 
         required=True,
         widget=forms.TextInput(attrs={
              "placeholder":"E-mail",
              'class':"form-control form-control-lg fs-6"
         })
    )
    
    password = forms.CharField(
         label="Palavra-passe", 
         required=True,
         widget=forms.PasswordInput(attrs={
              "placeholder":"Palavra-passe",
              'class':"form-control form-control-lg fs-6"
         })
    )
        
