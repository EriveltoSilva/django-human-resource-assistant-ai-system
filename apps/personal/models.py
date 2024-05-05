import uuid
from django.db import models
from django.contrib.auth import get_user_model

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
    