import re
from .. import utils
from django import forms
from django.utils import timezone 
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ..models import Sector

User = get_user_model()

def is_email_valid(email:str)->bool:
  """ Função para validar um endereço de email."""
  regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,7}$'     # Expressão regular para um email válido
  return re.match(regex, email)                                 # Retorna True se o email corresponder à expressão regular

def add_attr(field, attr_name, attr_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_val}'.strip()

def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = f'{placeholder_val}'.strip()


class SignupBusinessForm(forms.ModelForm):
    class Meta:
        model = User
        fields =[
            'first_name', 'username',
            'email', 'nif', 'sector','phone', 'address','website', 
            'password', 'password2']

    
    first_name = forms.CharField(
        label="Nome",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder":"Nome da empresa",
            "class":"form-control form-control-lg fs-6",
            "iconClass":"person",
        }),
        error_messages={
            "required":"O campo nome não pode estar vazio!" 
        },
    )

    # last_name = forms.CharField(
    #     label="Sobrenome",
    #     required=True,
    #     max_length=100,
    #     widget=forms.TextInput(attrs={
    #         "placeholder":"Sobrenome",
    #         "class":"form-control form-control-lg fs-6",
    #         "iconClass":"person",
    #     })
    # )

    username = forms.CharField(
        label="Username",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder":"Username",
            "class":"form-control form-control-lg fs-6",
            "iconClass":"person",
        }),
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        max_length=100,
        widget=forms.EmailInput(attrs={
            "placeholder":"E-mail",
            "class":"form-control form-control-lg fs-6",
            "iconClass":"envelope", 
        }),
        error_messages={
            'required': 'Este campo é obrigatório' }
    )

    nif = forms.CharField(
        label="Nº de Identificação Fiscal",
        required=True,
        max_length=14,
        widget=forms.TextInput(attrs={
            "placeholder":"Nif", 
            "class":"form-control form-control-lg fs-6",
            "iconClass":"person", 
        }), 
    )
    

    sector = forms.ModelChoiceField(
        label='Sector',
        required=True,
        queryset=Sector.objects.all(),
        widget=forms.Select(attrs={
            "placeholder":"Sector", 
            "class":"form-select form-control-lg fs-6",
            "iconClass":"company", 
        }), 
    )


    phone = forms.CharField(
        label="Telefone",
        required=True,
        max_length=13,
        widget=forms.TextInput(attrs={
            'type': 'tel',
            "placeholder":"Telefone",
            "class":"form-control form-control-lg fs-6",
            "iconClass":"telephone",
        })
    )

    address = forms.CharField(
        label="Endereço",
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={
            "placeholder":"Endereço", 
            "class":"form-control form-control-lg fs-6",
            "iconClass":"house", 
        }), 
    )
    
    website = forms.URLField(
        label="Website",
        required=True,
        max_length=255,
        widget=forms.URLInput(attrs={
            "placeholder":"Ex.:https://company.com", 
            "class":"form-control form-control-lg fs-6",
            "iconClass":"globe", 
        }), 
    )

    password = forms.CharField(
        label='Senha',
        required=True,
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Palavra-passe",
                "class":"form-control form-control-lg fs-6",
                "iconClass":"lock",
            }
        ),
    )

    password2 = forms.CharField(
        label='Senha de Confirmação',
        required=True,
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Confirmar Palavra-passe",
                "class":"form-control form-control-lg fs-6",
                "iconClass":"lock",
            }
        ),
    )
    
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
    
    
    def clean_nif(self):
        nif = self.cleaned_data.get('nif').strip()
        if len(nif) != 14:
            raise ValidationError("O número de identificação deve ter 14 caracteres.")
        return nif
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone').strip()
        if phone:   
            if "+244" not in phone:
                phone = "+244"+ phone
            if not re.match(r'^\+244\d{9}$', phone):
                raise ValidationError("O número de telefone deve conter 9 digitos.")
        return phone
    
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
