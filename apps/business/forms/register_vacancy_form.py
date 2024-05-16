"""register form for vacancy

Raises:
    ValidationError: expiration date can not be in a past date
    ValidationError: The minimum salary cannot be higher than the maximum salary
    ValidationError: The maximum salary cannot be lower than the minimum salary
    ValidationError: _description_
    ValidationError: _description_

Returns:
    _type_: _description_
"""
from django import forms
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ..models import Vacancy, JobType

User = get_user_model()

class RegisterVacancyForm(forms.ModelForm):
    """register vacancy form model"""
    class Meta:
        model = Vacancy
        fields = [
            'title', 'job_type', 'description', 
            'city', 'expiration_data', 'min_wage', 'max_wage', 
            'entry_time', 'exit_time']

    title = forms.CharField(
        label="Cargo",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder":"Cargo",
            "class":"form-control",
            "tamanho":"col-12 col-sm-6 mt-4",
        }),
        error_messages={
            "required":"O campo Cargo não pode estar vazio!" 
        },
    )

    job_type = forms.ModelChoiceField(
        label='Tipo de Trabalho',
        required=True,
        queryset=JobType.objects.all(),
        widget=forms.Select(attrs={
            "placeholder":"Tipo de Trabalho", 
            "class":"form-control",
            "tamanho":"col-12 col-sm-6 mt-4", 
        }),
    )

    description = forms.CharField(
        label="Descrição",
        required=True,
        widget=forms.Textarea(attrs={
            "placeholder":"Descrição",
            "class":"form-control",
            "tamanho":"col-12 mt-4", 
        })
    )

    city = forms.CharField(
        label="Cidade",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder":"Cidade",
            "class":"form-control form-control-lg fs-6",
            "tamanho":"col-12 col-sm-6 mt-4", 
        }),
    )

    expiration_data = forms.DateField(
        label='Data Limite de Contratação',
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'format':"%H/%M", 
            'class':'form-control form-control-lg fs-6',
            "tamanho":"calendar2-date col-12 col-sm-6 mt-4",
        }),
        error_messages={
            "required":"O campo Data de reunião não pode estar vazio!" },
    )

    min_wage = forms.DecimalField(
        label="Mínimo Salarial(kz)",
        required=True,
        widget=forms.NumberInput(attrs={
            "placeholder":"Mínimo Salário",
            "class":"form-control",
            "tamanho":"col-12 col-sm-6 mt-4",
        }),
        error_messages={
            "required":"O campo 'mínimo salarial' não pode estar vazio!" 
        },
    )

    max_wage = forms.DecimalField(
        label="Máximo Salarial(kz)",
        required=True,
        widget=forms.NumberInput(attrs={
            "placeholder":"Máximo Salarial",
            "class":"form-control",
            "tamanho":"col-12 col-sm-6 mt-4",
        }),
        error_messages={
            "required":"O campo 'máximo salarial'  não pode estar vazio!" 
        },
    )

    entry_time = forms.TimeField(
        label='Hora de Início de Trabalho',
        required=True,
        widget=forms.TimeInput(attrs={
            'format':"%H/%M",
            'type': 'time',
            'class':'form-control',
            "tamanho":"col-12 col-sm-6 mt-4",
        })
    )

    exit_time = forms.TimeField(
        label='Hora de Saída do Trabalho',
        required=True,
        widget=forms.TimeInput(attrs={
            'format':"%H/%M",
            'type': 'time',
            'class':'form-control',
            "tamanho":"col-12 col-sm-6 mt-4",
        })
    )

    def clean_title(self):
        """remove the whitespaces at the end of string"""
        return self.cleaned_data.get('title').strip()

    def clean_description(self):
        """remove the whitespaces at the end of string"""
        return self.cleaned_data.get('description').strip()

    def clean_address(self):
        """remove the whitespaces at the end of string"""
        return self.cleaned_data.get('address').strip()

    def clean_expiration_data(self):
        """remove the whitespaces at the end of string"""
        expiration_data = self.cleaned_data.get('expiration_data')
        if expiration_data and expiration_data <= timezone.now().date():
            raise ValidationError("A data de expiração deve estar no futuro!", "invalid")
        return expiration_data

    def clean_min_wage(self):
        """verify if min_wage is higher than 0"""
        min_wage = self.cleaned_data.get('min_wage')
        if min_wage <= 0:
            raise ValidationError("O mínimo salarial deve ser maior que zero!", "invalid")
        return min_wage

    def clean_max_wage(self):
        """verify if max_wage is higher than 0"""
        max_wage = self.cleaned_data.get('max_wage')
        if max_wage <= 0 :
            raise ValidationError("O máximo salarial deve ser maior que zero!", "invalid")
        return max_wage

    def clean(self):
        """verify:
        1- if min_wage if lower than max_wage
        2- if entry_time is a before date than exit_time
        """
        cleaned_data = super().clean()
        min_wage = cleaned_data.get("min_wage")
        max_wage =  cleaned_data.get("max_wage")

        entry_time = self.cleaned_data.get('entry_time')
        exit_time = self.cleaned_data.get('exit_time')

        if min_wage > max_wage:
            raise ValidationError({
                'min_wage': "Os campo minimo salarial  não pode ser maior que o máximo salario!",
                'max_wage': "Os campo minimo salarial não pode ser maior que o máximo salario!"})

        if entry_time > exit_time:
            raise ValidationError({
                'entry_time':"A hora de saída é anterior a hora de entrada",
                'exit_time': "A hora de saída é anterior a hora de entrada"})
