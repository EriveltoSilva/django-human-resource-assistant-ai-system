""" Business Models """

import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class JobType(models.Model):
    """job type for representing like remote, presencial, hybrid etc...
    Args:
        models (Model): ORM model
    """
    title = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Tipo de Trabalho'
        ordering = ['title', '-created_at']

    def __str__(self) -> str:
        return f"{self.title}"

class Vacancy(models.Model):
    """vacancy model"""
    vid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    image = models.ImageField(upload_to="perfil", blank=True)
    job_type = models.ForeignKey(JobType, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    city = models.CharField(max_length=255)
    min_wage = models.DecimalField(max_digits=15, decimal_places=2)
    max_wage = models.DecimalField(max_digits=15, decimal_places=2)
    expiration_data = models.DateField()
    entry_time = models.TimeField()
    exit_time = models.TimeField()
    is_published = models.BooleanField(default=True)

    company = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Vagas'
        ordering = ['-created_at', 'title']

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        """gets url for vacancy profile
        Returns:
            str: url string for vacancy 
        """
        return reverse("business:vacancy-detail", kwargs={"company_slug": self.company.slug,
                                                            "vid":self.vid})

    def image_url(self):
        """ image url string
        Returns:
            str: image url 
        """
        try:
            url = self.image.url
        except ValueError:
            url = self.company.company_profile.image_url
        return url

    def get_skills(self):
        """get all skills required for this vacancy
        Returns:
            Queryset: vacancy skills queryset
        """
        return Skill.objects.filter(vacancy=self)

    def get_responsibilities(self):
        """get all responsibilities required for this vacancy
        Returns:
            Queryset: vacancy responsibilities queryset
        """
        return Responsibility.objects.filter(vacancy=self)

    def get_benefits(self):
        """get all benefits required for this vacancy
        Returns:
            Queryset: vacancy benefits queryset
        """
        return Benefit.objects.filter(vacancy=self)

class Benefit(models.Model):
    """ model for employment benefits for the person hiring for the position """
    bid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Beneficios de Trabalho'
        ordering = ['title', '-created_at']

    def __str__(self) -> str:
        return f"{self.title}"

class Skill(models.Model):
    """ skill model """
    sid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Habilidades Requeridas'
        ordering = ['title', '-created_at']

    def __str__(self) -> str:
        return f"{self.title}"

class Responsibility(models.Model):
    """model responsibility for a detail """
    rid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Responsabilidades'
        ordering = ['title', '-created_at']

    def __str__(self) -> str:
        return f"{self.title}"

class Candidate(models.Model):
    """register vacancy candidates"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    cv = models.FileField(upload_to="candidates/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Candidaturas'
        ordering = ['user', '-created_at']

    def __str__(self) -> str:
        return f"{self.user.get_full_name()}-{self.vacancy.title}"

    def get_absolute_url(self):
        """return the candidate string url"""
        return reverse("model_detail", kwargs={"pk": self.pk})
