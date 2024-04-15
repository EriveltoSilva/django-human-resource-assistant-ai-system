from . import utils
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class Sector(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name', 'created_at']
        verbose_name_plural = "Sectores Empresarial"
    
    def __str__(self) -> str:
        return self.name

    
class AbstractProfile(models.Model):
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="perfil", blank=True)
    phone = models.CharField(max_length=13, unique=True, null=True)
    address = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class PersonalProfile(AbstractProfile):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="personal_profile")
    bi = models.CharField(max_length=14, null=False, unique=True)
    gender = models.CharField(max_length=50, choices=utils.GENDER, default=utils.GENDER[0])
    birthday = models.DateField(null=True,blank=True)


    class Meta:
        verbose_name_plural = "Perfils de Usuários"
        ordering = ["user"]

    def __str__(self) -> str:
        return self.get_full_name()
    
    def get_full_name(self) -> str:
        return self.user.get_full_name()
    
    def get_gender(self):
        """Retorna a representação amigável para exibição do campo 'gender'."""
        return [item for item in (utils.GENDER) ]

    def get_absolute_url(self):
        return reverse("edit-user", kwargs={"slug": self.slug})



class CompanyProfile(AbstractProfile):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="company_profile")
    sector = models.ForeignKey(Sector, models.PROTECT)
    nif = models.CharField(max_length=14, null=False, unique=True)
    website = models.URLField(max_length=255,blank=True)
    
    class Meta:
        verbose_name_plural = "Perfils Empresariais"
        ordering = ["user"]

    def __str__(self) -> str:
        return self.get_full_name()
    
    def get_full_name(self) -> str:
        return self.user.get_full_name()
    

    def get_absolute_url(self):
        return reverse("edit-user", kwargs={"slug": self.slug})
    