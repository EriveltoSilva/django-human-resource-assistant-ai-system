"""register form for vacancy skills"""

from django import forms
from ..models import Benefit


class VacancyBenefitForm(forms.ModelForm):
    """register vacancy benefit form model"""
    class Meta:
        model = Benefit
        fields = ['title']

    title = forms.CharField(
        label="Curta Descrição",
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={
            "placeholder":"Descrição",
            "class":"form-control",
            "tamanho":"col-12 mt-4",
        }),
        error_messages={
            "required":"O campo Descrição não pode estar vazio!" 
        },
    )

    def clean_title(self):
        """remove the whitespaces at the end of string"""
        return self.cleaned_data.get('title').strip()
