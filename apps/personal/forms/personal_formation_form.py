import re
from django import forms
from apps.accounts import utils
from django.utils import timezone 
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ..models import AcademicInstituition, ProfissionalInstituition, AcademicFormationItem, ProfissionalFormationItem

# from django.contrib.auth.models import User
User = get_user_model()

class ProfissionalFormationForm(forms.ModelForm):
    class Meta:
        model = ProfissionalFormationItem
        fields = ["title", "hours", "institution", "year",]
        

    title = forms.CharField(
        label="Titulo",
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={
            "placeholder":"Nome do Curso ou Certificação", 
            "class":"form-control",
        }), 
    )

    institution = forms.ModelChoiceField(
        label='Instituição',
        required=True,
        queryset = ProfissionalInstituition.objects.all(),
        widget=forms.Select(attrs={
            "placeholder":"Instituição", 
            "class":"form-control form-control-xl fs-6 ",
            "iconClass":"company", 
        }), 
    )

    # code = forms.CharField(
    #     label="Código",
    #     required=True,
    #     max_length=255,
    #     widget=forms.TextInput(attrs={
    #         "placeholder":"Nome do Curso ou Certificação", 
    #         "class":"form-control",
    #     }), 
    # )

    hours = forms.IntegerField(
        label="Número de Horas",
        required=True,
        widget=forms.NumberInput(attrs={
            "placeholder":"Nº de Horas", 
            "class":"form-control",
            "min":1,
            "max":1000000,
        }), 
    )
    year = forms.IntegerField(
        label="Ano",
        required=True,
        widget=forms.NumberInput(attrs={
            "placeholder":"Ano", 
            "class":"form-control",
            "min":1970,
            "max":2070,

        }), 
    )
    
    def clean_title(self):
        title = self.cleaned_data.get('title').strip()
        return title
    
    def clean_hours(self):
        hours = self.cleaned_data.get('hours')
        if hours < 1:
            raise ValidationError("O curso deve ter pelo menos 1 hora de duração")
        return hours
    
    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year > timezone.now().date().year:
            raise ValidationError("O ano de conclusão do cusrso não pode ser superior ao ano actual")
        return year
    


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
        label='Instituição',
        required=True,
        queryset = AcademicInstituition.objects.all(),
        widget=forms.Select(attrs={
            "placeholder":"Instituição", 
            "class":"form-control form-control-lg fs-6",
            "iconClass":"company", 
        }), 
    )

    start_year = forms.IntegerField(
        label="Ano de Início",
        required=True,
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
        widget=forms.NumberInput(attrs={
            "placeholder":"Ano de Termino", 
            "class":"form-control",
            "min":1970,
            "max":2070,
        }), 
    )

        
    def clean_start_year(self):
        start_year = self.cleaned_data.get('start_year')
        if start_year > timezone.now().date().year:
            raise ValidationError("O ano de inicio não pode ser superior ao ano actual")
        return start_year
    
    def clean_end_year(self):
        end_year = self.cleaned_data.get('end_year')
        if end_year < 1970 or end_year > 2050:
            raise ValidationError("O ano de término inválido")
        return end_year
    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     start_year =  cleaned_data.get("start_year")
    #     end_year = cleaned_data.get("end_year")
        
    #     if start_year >= end_year:
    #         raise ValidationError({
    #             'start_year': "O ano de término deve ser maior que o ano de início",
    #             'end_year': "O ano de término deve ser maior que o ano de início",
    #         })
    

