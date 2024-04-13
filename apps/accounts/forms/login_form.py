from django import forms
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(
         label="Username", 
         required=True,
         widget=forms.TextInput(attrs={
              "placeholder":"Username",
              'class':"form-control form-control-lg fs-6"
         })
    )
    
    password = forms.CharField(
         label="Senha", 
         required=True,
         widget=forms.PasswordInput(attrs={
              "placeholder":"Senha",
              'class':"form-control form-control-lg fs-6"
         })
    )
        
