from typing import Iterable
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class ProfissionalExperience(models.Model):
    pid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Experiências Profissional"
        ordering = ['user']

    def __str__(self) -> str:
        return f"Experência - {self.user}"

class ProfissionalExperienceItem(models.Model):
    pid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    institution = models.CharField(max_length=255, null=True, blank=False)
    description = models.TextField()
    years = models.PositiveIntegerField()
    
    
    profissional_experience = models.ForeignKey(ProfissionalExperience, on_delete=models.CASCADE, related_name="profissional_experience_item")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Item Experiências Profissional"
        ordering = ['institution']
    def __str__(self) -> str:
        return f"Experência - {self.name}"


class AcademicInstituition(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    aid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Instituições Acadêmicas"
        ordering = ['name']
    def __str__(self) -> str:
        return self.name

class ProfissionalInstituition(models.Model):
    pid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Instituições Profissionais"
        ordering = ['name']
    def __str__(self) -> str:
        return self.name

class Formation(models.Model):
    fid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Formações"
        ordering = ['user']
    def __str__(self) -> str:
        return ("Formação de %s" % (self.user))

class AcademicFormationItem(models.Model):
    aid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    course = models.CharField(max_length=255, null=True, blank=True)
    institution = models.ForeignKey(AcademicInstituition, on_delete=models.PROTECT)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()
    is_finished = models.BooleanField(default=False)

    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name="academic_formation")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Formação Acadêmica"
        ordering = ['course']
    def __str__(self) -> str:
        return f"{self.course}"
    
    def get_finished_status(self):
        return "SIM" if self.is_finished else "NÂO"

class ProfissionalFormationItem(models.Model):
    pid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    institution = models.ForeignKey(ProfissionalInstituition, on_delete=models.PROTECT)
    # code = models.CharField(max_length=255,blank=True)
    hours = models.DecimalField(max_digits=7, decimal_places=2)
    year = models.PositiveIntegerField()

    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Formação Profissional"
        ordering = ['title']
    def __str__(self) -> str:
        return f"{self.title}"
    


def function_upload_to(instance, filename):
    # Substitua 'documents' pelo nome da pasta onde deseja armazenar os arquivos
    # e instance.case.title pelo nome da pasta que deseja criar com base no atributo 'case'
    return f"documents/{instance.user.username}/{filename}"

class Documentation(models.Model):
    did = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bi = models.FileField(upload_to=function_upload_to)
    cv = models.FileField(upload_to=function_upload_to)
    certificate_literary = models.FileField(upload_to=function_upload_to)
    medical_certificate = models.FileField(upload_to=function_upload_to, null=True, blank=True)
    other_doc1 = models.FileField(upload_to=function_upload_to, null=True, blank=True)
    other_doc2 = models.FileField(upload_to=function_upload_to, null=True, blank=True)
    other_doc3 = models.FileField(upload_to=function_upload_to, null=True, blank=True)
    other_doc4 = models.FileField(upload_to=function_upload_to, null=True, blank=True)
    other_doc5 = models.FileField(upload_to=function_upload_to, null=True, blank=True)
    other_doc6 = models.FileField(upload_to=function_upload_to, null=True, blank=True)
    other_doc7 = models.FileField(upload_to=function_upload_to, null=True, blank=True)
    other_doc8 = models.FileField(upload_to=function_upload_to, null=True, blank=True)
    other_doc9 = models.FileField(upload_to=function_upload_to, null=True, blank=True)
    other_doc10 =models.FileField(upload_to=function_upload_to, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    
    class Meta:
        verbose_name_plural = "Documentos"
        ordering = ['user', '-created_at',]
        
        
    def __str__(self) -> str:
        return f"Doc-{self.user}"
    
    def get_absolute_url(self):
        return self.file.url

    def get_pdf_conversation_url(self):
        return reverse("chat:conversation-pdf", args=(self.did,))
    
    def get_file_details(self):
        file_name = self.file.name.split('/')[-1] # obtém o nome do arquivo puro, 
        file_path = self.file.path # Obtém o caminho completo do arquivo
        file_size = self.file.size # Obtém o tamanho do arquivo em bytes
        file_id = self.id          # Obtém o ID do arquivo (no banco de dados)
        file_type = self.file.name.split('.')[-1]  # Obtém o tipo de arquivo (extensão) 
        return {'name': file_name[0], 'path': file_path, 'size': file_size, 'id': file_id, 'type': file_type}

    @property
    def get_bi(self):
        try:
            url = self.bi.url
        except:
            url = ""
        return url
    
    @property
    def get_cv(self):
        try:
            url = self.cv.url
        except:
            url = ""
        return url
    
    @property
    def get_certificate_literary(self):
        try:
            url = self.certificate_literary.url
        except:
            url = ""
        return url
    
    @property
    def get_medical_certificate(self):
        try:
            url = self.medical_certificate.url
        except:
            url = ""
        return url
    
    @property
    def get_other_doc1(self):
        try:
            url = self.other_doc1.url
        except:
            url = ""
        return url
    
    @property
    def get_other_doc2(self):
        try:
            url = self.other_doc2.url
        except:
            url = ""
        return url
    
    @property
    def get_other_doc3(self):
        try:
            url = self.other_doc3.url
        except:
            url = ""
        return url
    
    @property
    def get_other_doc4(self):
        try:
            url = self.other_doc4.url
        except:
            url = ""
        return url
    
    @property
    def get_other_doc5(self):
        try:
            url = self.other_doc5.url
        except:
            url = ""
        return url
    @property
    def get_other_doc6(self):
        try:
            url = self.other_doc6.url
        except:
            url = ""
        return url
    

    @property
    def get_other_doc7(self):
        try:
            url = self.other_doc7.url
        except:
            url = ""
        return url
    

    @property
    def get_other_doc8(self):
        try:
            url = self.other_doc8.url
        except:
            url = ""
        return url
    

    @property
    def get_other_doc9(self):
        try:
            url = self.other_doc9.url
        except:
            url = ""
        return url
    

    @property
    def get_other_doc10(self):
        try:
            url = self.other_doc10.url
        except:
            url = ""
        return url
    