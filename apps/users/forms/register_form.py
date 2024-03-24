import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def is_email_valid(email:str)->bool:
  """
  Função para validar um endereço de email.
  Args:
    email: O endereço de email a ser validado.
  Returns:
    True se o email for válido, False caso contrário.
  """
  regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,7}$'     # Expressão regular para um email válido
  return re.match(regex, email)                                 # Retorna True se o email corresponder à expressão regular

def add_attr(field, attr_name, attr_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_val}'.strip()

def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = f'{placeholder_val}'.strip()

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs)->None:
        super().__init__(*args, **kwargs)
        # add_attr(self.fields['username'], 'placeholder', 'Hello')
        # add_placeholder(self.fields['username'],  'wprçd')
    
    first_name = forms.CharField(
        label="Primeiro Nome",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder":"Insira o seu primeiro nome",
            "class":"form-control form-control-lg"
        }),
        error_messages={
            "required":"O campo primeiro nome não pode estar vazio!" 
        },
    )

    last_name = forms.CharField(
        label="Sobrenome",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder":"Insira o seu sobrenome","fatherClass":"form-group", "class":"form-control form-control-lg"})
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        max_length=100,
        widget=forms.EmailInput(attrs={"placeholder":"Insira o seu email","fatherClass":"form-group", "class":"form-control"}),
        error_messages={
            'required': 'Este campo é obrigatório' }
    )

    username = forms.CharField(
        label="Username",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder":"Insira o seu username","fatherClass":"form-group", "class":"form-control"}),
        # help_text="O username não pode conter espaços em branco"
        # error_messages={
        #     'invalid':'O username não pode ter espaços em branco-e'
        # }
    )

    password = forms.CharField(
        label='Senha',
        required=True,
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Insira a sua senha",
                "fatherClass":"form-group",
                "class":"form-control"
            }
        ),
    )

    password2 = forms.CharField(
        label='Senha de Confirmação',
        required=True,
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Insira a sua senha novamente",
                "fatherClass":"form-group",
                "class":"form-control"
            }
        ),
    )


    class Meta:
        model=User
        fields =['first_name', 'last_name', 'email', 'username', 'password']

    def clean_first_name(self):
        return self.cleaned_data.get('first_name').strip()
    
    def clean_last_name(self):
        return self.cleaned_data.get('last_name').strip()
    
    def clean_email(self):
        email = self.cleaned_data.get('email').strip()
        if not is_email_valid(email):
            raise ValidationError("Este email é inválido", code='invalid')
        elif User.objects.filter(email=email).exists():
            raise ValidationError("Já existe um usuário com este email", code='invalid')

        return email
    
    def clean_username(self):
        data = self.cleaned_data.get('username').strip()
        if ' ' in data:
            raise ValidationError("O username não pode conter espaços em branco",code='invalid')
        return data
    
    def clean(self):
        cleaned_data = super().clean()
        password =  cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        
        if password != password2:
            raise ValidationError({
                'password': "Os campos de senha devem ser iguais",
                'password2': "Os campos de senha devem ser iguais"})
        elif len(password) < 8:
            raise ValidationError({
                'password': "As senhas devem ter no minimo 8 caracteres",
                'password2': "As senhas devem ter no minimo 8 caracteres"})
