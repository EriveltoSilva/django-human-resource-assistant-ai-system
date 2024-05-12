from django import forms
from django.utils import timezone
from ..models import Vacancy, JobType
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class RegisterVacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = [
            'title', 'job_position', 'description', 
            'address', 'expiration_data', 'min_wage', 'max_wage', 
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

    job_position = forms.ModelChoiceField(
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

    address = forms.CharField(
        label="Endereço",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder":"Endereço",
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
        label="Salário Mínino",
        required=True,
        widget=forms.NumberInput(attrs={
            "placeholder":"Salário Mínino",
            "class":"form-control",
            "tamanho":"col-12 col-sm-6 mt-4",
        }),
        error_messages={
            "required":"O campo salário mínino não pode estar vazio!" 
        },
    )
    
    max_wage = forms.DecimalField(
        label="Salário Máximo",
        required=True,
        widget=forms.NumberInput(attrs={
            "placeholder":"Salário Máximo",
            "class":"form-control",
            "tamanho":"col-12 col-sm-6 mt-4",
        }),
        error_messages={
            "required":"O campo salário máximo não pode estar vazio!" 
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
        return self.cleaned_data.get('title').strip()
    
    def clean_description(self):
        return self.cleaned_data.get('description').strip()
    
    def clean_address(self):
        return self.cleaned_data.get('address').strip()
    
    def clean_address(self):
        return self.cleaned_data.get('address').strip()
    
    def clean_expiration_data(self):
        expiration_data = self.cleaned_data.get('expiration_data')
        if expiration_data and expiration_data <= timezone.now().date():
            raise ValidationError("A data de expiração deve estar no futuro!", "invalid")
        return expiration_data
    
    def clean_min_wage(self):
        min_wage = self.cleaned_data.get('min_wage')
        if min_wage <= 0:
            raise ValidationError("O salário mínimo deve ser maior que zero!", "invalid")
        return min_wage
    
    def clean_max_wage(self):
        max_wage = self.cleaned_data.get('max_wage')
        if max_wage <= 0 :
            raise ValidationError("O salário máximo deve ser maior que zero!", "invalid")
        return max_wage
    

    def clean(self):
        cleaned_data = super().clean()
        min_wage = cleaned_data.get("min_wage")
        max_wage =  cleaned_data.get("max_wage")

        entry_time = self.cleaned_data.get('entry_time')
        exit_time = self.cleaned_data.get('exit_time')
        
        if min_wage > max_wage:
            raise ValidationError({
                'min_wage': "Os campo salario minimo não pode ser maior que o salario máximo!",
                'max_wage': "Os campo salario minimo não pode ser maior que o salario máximo!"})
        
        if entry_time > exit_time:
            raise ValidationError({
                'entry_time':"A hora do término é anterior a hora de início",
                'exit_time': "A hora do término é anterior a hora de início"})