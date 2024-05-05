import re
from django import forms
from apps.accounts import utils
from django.utils import timezone 
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ..models import AcademicInstituition,Formation, AcademicFormationItem, ProfissionalFormationItem

# from django.contrib.auth.models import User
User = get_user_model()

class AcademicFormationForm(forms.ModelForm):
    class Meta:
        model = AcademicFormationItem
        fields = ["course", "institution", "start_year", "end_year", "is_finished",]
        

    course = forms.CharField(
        label="Curso",
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={
            "placeholder":"Curso", 
            "class":"form-control",
        }), 
    )

    institution = forms.ModelChoiceField(
        label='Sector',
        required=True,
        queryset = AcademicInstituition.objects.all(),
        widget=forms.Select(attrs={
            "placeholder":"Sector", 
            "class":"form-control form-control-lg fs-6",
            "iconClass":"company", 
        }), 
    )

    start_year = forms.IntegerField(
        label="Ano de Início",
        required=True,
        # max_length=14,
        widget=forms.NumberInput(attrs={
            "placeholder":"Ano de Início", 
            "class":"form-control",
            "min":1970,
            "max":2070,

        }), 
    )
    
    end_year = forms.IntegerField(
        label="Ano de Termino",
        required=True,
        # max_length=14,
        widget=forms.NumberInput(attrs={
            "placeholder":"Ano de Termino", 
            "class":"form-control",
            "min":1970,
            "max":2070,
        }), 
    )

    


    
    # def clean_phone(self):
    #     phone = self.cleaned_data.get('phone').strip()
    #     if phone:   
    #         if "+244" not in phone:
    #             phone = "+244"+ phone
    #         if not re.match(r'^\+244\d{9}$', phone):
    #             raise ValidationError("O número de telefone deve conter 9 digitos.")
    #     return phone

