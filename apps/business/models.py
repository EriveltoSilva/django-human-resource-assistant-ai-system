import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class JobType(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Tipo de Trabalho'
        ordering = ['title', '-created_at']

class Vacancy(models.Model):
    vid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    job_position = models.ForeignKey(JobType, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    address = models.CharField(max_length=255)
    min_wage = models.DecimalField(max_digits=15, decimal_places=2)
    max_wage = models.DecimalField(max_digits=15, decimal_places=2)
    expiration_data = models.DateField()
    entry_time = models.TimeField()
    exit_time = models.TimeField()
    is_published = models.BooleanField(default=True)
    
    company = models.ForeignKey(User, on_delete=models.CASCADE)
    # benefits = models.CharField(max_length=100)
    # skills = models.ManyToManyField(Skill,blank=False)
    # responsabilities = models.ManyToManyField(Responsability,blank=False)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Vagas'
        ordering = ['-created_at', 'title']
    
    def __str__(self):
        return self.title
    
class Skill(models.Model):
    sid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Habilidades ou Competências'
        ordering = ['title', '-created_at']

    def __str__(self) -> str:
        return self.title

class Responsability(models.Model):
    rid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Responsabilidades'
        ordering = ['title', '-created_at']

    def __str__(self) -> str:
        return self.title