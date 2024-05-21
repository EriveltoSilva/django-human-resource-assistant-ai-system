from django import forms
from ..models import Documentation
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# from django.contrib.auth.models import User
User = get_user_model()

class PersonalDocumentationForm(forms.ModelForm):
    class Meta:
        model = Documentation
        fields = [
            "bi", 
            "cv", 
            "certificate_literary", 
            "medical_certificate", 
            "other_doc1", 
            "other_doc2", 
            "other_doc3", 
            "other_doc4", 
            "other_doc5", 
            "other_doc6", 
            "other_doc7", 
            "other_doc8", 
            "other_doc9", 
            "other_doc10", 
        ]

    bi = forms.FileField(
        label='Bilhete de Identidade',
        required=True,
        widget=forms.FileInput(attrs={"class":"file-upload-default", "accept":"image/*,application/pdf"}),
        help_text="*" 
    )
    
    cv = forms.FileField(
        label='Curriculum Vitae',
        required=True,
        widget=forms.FileInput(attrs={"class":"file-upload-default", "accept":"image/*,application/pdf"}), 
        help_text="*" 
    )
    
    certificate_literary = forms.FileField(
        label='Certificado de Habilitações Literais',
        required=True,
        widget=forms.FileInput(attrs={"class":"file-upload-default", "accept":"image/*,application/pdf"}), 
        help_text="*" 
    )
    
    medical_certificate = forms.FileField(
        label='Atestado Médico',
        required=False,
        widget=forms.FileInput(attrs={"class":"file-upload-default", "accept":"image/*,application/pdf"}), 
    )
    
    other_doc1 = forms.FileField(
        label='Outro Documentos 1',
        required=False,
        widget=forms.FileInput(attrs={"class":"file-upload-default", "accept":"image/*,application/pdf"}), 
    )
    other_doc2 = forms.FileField(
        label='Outro Documentos 2',
        required=False,
        widget=forms.FileInput(attrs={"class":"file-upload-default", "accept":"image/*,application/pdf"}), 
    )
    other_doc3 = forms.FileField(
        label='Outro Documentos 3',
        required=False,
        widget=forms.FileInput(attrs={"class":"file-upload-default", "accept":"image/*,application/pdf"}), 
    )
    other_doc4 = forms.FileField(
        label='Outro Documentos 4',
        required=False,
        widget=forms.FileInput(attrs={"class":"file-upload-default", "accept":"image/*,application/pdf"}), 
    )
    other_doc5 = forms.FileField(
        label='Outro Documentos 5',
        required=False,
        widget=forms.FileInput(attrs={"class":"file-upload-default", "accept":"image/*,application/pdf"}), 
    )
    other_doc6 = forms.FileField(
        label='Outro Documentos 6',
        required=False,
        widget=forms.FileInput(attrs={"class":"file-upload-default", "accept":"image/*,application/pdf"}), 
    )

    other_doc7 = forms.FileField(
        label='Outro Documentos 7',
        required=False,
        widget=forms.FileInput(attrs={"class":"file-upload-default", "accept":"image/*,application/pdf"}), 
    )
    
    other_doc8 = forms.FileField(
        label='Outro Documentos 8',
        required=False,
        widget=forms.FileInput(attrs={"class":"file-upload-default", "accept":"image/*,application/pdf"}), 
    )

    other_doc9 = forms.FileField(
        label='Outro Documentos 9',
        required=False,
        widget=forms.FileInput(attrs={"class":"file-upload-default", "accept":"image/*,application/pdf"}), 
    )

    other_doc10 = forms.FileField(
        label='Outro Documentos 10',
        required=False,
        widget=forms.FileInput(attrs={"class":"file-upload-default", "accept":"image/*,application/pdf"}), 
    )

    