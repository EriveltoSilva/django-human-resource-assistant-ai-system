from django import forms
from django.contrib.auth import get_user_model
from ..models import ProfissionalExperienceItem

User = get_user_model()

class ProfissionalExperienceForm(forms.ModelForm):
    class Meta:
        model = ProfissionalExperienceItem
        fields = ["institution", "years", "description",]
        
    institution = forms.CharField(
        label="Instituição",
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={
            "placeholder":"Instituição onde trabalhou", 
            "class":"form-control",
        }), 
    )

    years = forms.IntegerField(
        label="Quantos anos de trabalho",
        required=True,
        widget=forms.NumberInput(attrs={
            "placeholder":"Nº de Horas", 
            "class":"form-control",
            "min":0,
            "max":80,
        }), 
    )
    
    description = forms.CharField(
        label="Descrição",
        required=True,
        widget=forms.Textarea(attrs={
            "placeholder":"Fale sobre o trabalho que realizou, a experiência que obteve", 
            "class":"form-control",
        }), 
    )

    
    def clean_institution(self):
        institution = self.cleaned_data.get('institution').strip()
        return institution
    
    def clean_description(self):
        description = self.cleaned_data.get('description').strip()
        return description
    
