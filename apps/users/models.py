from . import utils
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# class Area(models.Model):
#     name=models.CharField(max_length=150,null=False, blank=False)
#     description = models.TextField(default="")
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         ordering = ["name"]

#     def __str__(self) -> str:
#         return str(self.name)
    

# class Profile(models.Model):
#     GENDER =(("MASCULINO", "MASCULINO"),("FEMININO", "FEMININO"),)
#     user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="profile")
#     # slug = models.SlugField(unique=True)
#     slug = models.SlugField()
#     gender = models.CharField(max_length=50, choices=GENDER, default=utils.GENDER[0])
#     birthday = models.DateField(null=True,blank=True)
#     hiring_date = models.DateField(null=True,blank=True)
#     area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True)  
#     image = models.ImageField(upload_to="lawyers", blank=True)
#     is_admin=models.BooleanField(default=False)
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="users_created")
#     updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="users_updated")
#     class Meta:
#         ordering = ["user"]

#     def __str__(self) -> str:
#         return self.get_full_name()
    
#     def get_full_name(self) -> str:
#         return self.user.get_full_name()
    
#     def get_create_by(self) -> str:
#         return f"{self.created_by.get_full_name()}"
    
#     def get_is_active(self) -> str:
#         return  "SIM" if self.user.is_active else "NÃO"
    
#     def get_is_superuser(self) -> str:
#         return  "SIM" if self.user.is_superuser else "NÃO"
    
#     def get_is_admin(self) -> str:
#         return  "SIM" if self.is_admin else "NÃO"
    
    
#     def has_superuser_permission(self) -> bool:
#         return  True if self.user.is_superuser else False
    
#     def has_director_permission(self) -> bool:
#         return  True if self.is_admin else False
    
#     def get_gender(self):
#         """Retorna a representação amigável para exibição do campo 'gender'."""
#         gender_dict = []
#         for item in (utils.GENDER):
#             gender_dict.append(item)
#         return gender_dict

    
#     def get_absolute_url(self):
#         return reverse("edit-user", kwargs={"slug": self.slug})
    