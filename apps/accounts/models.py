from . import utils
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="profile")
    slug = models.SlugField(unique=True)
    bi = models.CharField(max_length=14, null=False, unique=True)
    gender = models.CharField(max_length=50, choices=utils.GENDER, default=utils.GENDER[0])
    birthday = models.DateField(null=True,blank=True)
    image = models.ImageField(upload_to="perfil", blank=True)
    is_admin=models.BooleanField(default=False)

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
    