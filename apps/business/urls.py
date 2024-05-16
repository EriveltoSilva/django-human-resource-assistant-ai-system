""" Business urls for """
from django.urls import path
from . import views

app_name = "business"

urlpatterns = [
    path('home/', views.home, name="home"),
    path('apagar-vaga/<uuid:vid>/', views.delete_vacancy, name="delete-vacancy"),
    path('vagas/', views.vacancy_list, name="vacancy-list"),
    path('vagas/<slug:company_slug>/detalhes/<uuid:vid>/', views.vacancy_detail, name="vacancy-detail"),
    path('nova-vaga/', views.register_vacancy, name="register-vacancy"),
    path('candidaturas/', views.candidacy, name="candidacy"),
]