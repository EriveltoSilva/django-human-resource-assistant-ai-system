import re
from django import forms
from apps.accounts import utils
from django.utils import timezone 
from django.contrib.auth import get_user_model
from apps.accounts.models import PersonalProfile
from django.core.exceptions import ValidationError

# from django.contrib.auth.models import User
User = get_user_model()

class PersonalProfileInformationForm(forms.ModelForm):
    class Meta:
        model = PersonalProfile
        fields = ["bi", "birthday", "gender", "phone", "address", "image",]
        
    bi = forms.CharField(
        label="Nº do Bilhete",
        required=True,
        max_length=14,
        widget=forms.TextInput(attrs={
            "placeholder":"Nº do Bilhete", 
            "class":"form-control",
        }), 
    )

    birthday = forms.DateField(
        label='Data de Nascimento',
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'format':"%H/%M", 
            'class':'form-control form-control-lg fs-6',
            "iconClass":"calendar2-date",
        }),
        error_messages={
            "required":"O campo Data de reunião não pode estar vazio!" },
    )

    phone = forms.CharField(
        label="Telefone",
        required=True,
        max_length=13,
        widget=forms.TextInput(attrs={
            'type': 'tel',
            "placeholder":"Ex:940811141",
            "class":"form-control form-control-lg fs-6",
            "iconClass":"telephone",
        })
    )

    gender = forms.CharField(
        label="Gênero",
        required=True,
        max_length=50,
        widget=forms.Select(attrs={
            "class":"form-control",
            "iconClass":"gender-male",
            }, choices=utils.GENDER
        ), 
        error_messages={"required":"O campo genero não pode estar vazio!" },
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

    image = forms.ImageField(
        label='Imagem de Perfil',
        widget=forms.FileInput(attrs={
            "class":"form-control"}), 
    )

    def clean_bi(self):
        bi = self.cleaned_data.get('bi').strip()
        if len(bi) != 14:
            raise ValidationError("O número de identificação deve ter 14 caracteres.")
        return bi
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone').strip()
        if phone:   
            if "+244" not in phone:
                phone = "+244"+ phone
            if not re.match(r'^\+244\d{9}$', phone):
                raise ValidationError("O número de telefone deve conter 9 digitos.")
        return phone


class PersonalInformationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email',]
    
    first_name = forms.CharField(
        label="Primeiro Nome",
        widget=forms.TextInput(attrs={
            "placeholder":"Primeiro Nome",
            "class":"form-control form-control-lg fs-6",
            "readonly":True
        }),
        error_messages={
            "required":"O campo primeiro nome não pode estar vazio!" 
        },
    )

    last_name = forms.CharField(
        label="Sobrenome",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder":"Sobrenome",
            "class":"form-control form-control-lg fs-6",
            "readonly":True
        })
    )

    username = forms.CharField(
        label="Username",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder":"Username",
            "class":"form-control form-control-lg fs-6",
            "readonly":True
        }),
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        max_length=100,
        widget=forms.EmailInput(attrs={
            "placeholder":"E-mail",
            "class":"form-control",
            "readonly":True
        }),
        error_messages={
            'required': 'Este campo é obrigatório' }
    )

