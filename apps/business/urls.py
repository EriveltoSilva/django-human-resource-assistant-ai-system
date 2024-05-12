from django.urls import path
from . import views
app_name= "business"

urlpatterns = [
    path('home/', views.home, name="home"),
    path('vagas/', views.vacancy, name="vacancy"),
    path('nova-vaga/', views.register_vacancy, name="register-vacancy"),
    path('candidaturas/', views.candidacy, name="candidacy"),
]