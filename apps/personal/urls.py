from django.urls import path
from . import views
app_name= "personal"

urlpatterns = [
    path('perfil/actualizar/', views.profile_update, name="profile-update"),
    path('formacao/academica/nova/', views.add_academic_formation, name="add-academic-formation"),
    path('formacao/academica/deletar/<uuid:id>', views.delete_academic_formation, name="delete-academic-formation"),
    path('formacao/profissional/nova/', views.add_profissional_formation, name="add-profissional-formation"),
    path('formacao/profissional/deletar/<uuid:id>', views.delete_profissional_formation, name="delete-profissional-formation"),
    
    path('expericia-profissional/nova/', views.add_profissional_experience, name="add-profissional-experience"),
    

    path('home/', views.home, name="home"),
    path('minha-carreira-profissional/', views.career, name="career"),



    

    path('vagas/', views.home, name="opportunities"),
    path('candidaturas/', views.home, name="applications"),
    path('meu-emprego/', views.home, name="my-job"),
]
