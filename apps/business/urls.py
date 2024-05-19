""" Business urls for """
from django.urls import path
from . import views

app_name = "business"

urlpatterns = [
    path('home/', views.home, name="home"),
    path('vagas/', views.vacancy_list, name="vacancy-list"),
    path('vagas/nova-vaga/', views.register_vacancy, name="register-vacancy"),
    path('vagas/apagar-vaga/<uuid:vid>/', views.delete_vacancy, name="delete-vacancy"),
    path('vagas/adicionar-requisito/<uuid:vid>/', views.add_vacancy_skills, name="add-vacancy-skill"),
    path('vagas/adicionar-responsabilidade/<uuid:vid>/', views.add_vacancy_responsibilities, name="add-vacancy-responsibility"),
    path('vagas/adicionar-beneficio/<uuid:vid>/', views.add_vacancy_benefits, name="add-vacancy-benefits"),

    path('vagas/edit-vaga/<uuid:vid>/', views.edit_vacancy, name="edit-vacancy"),
    path('vagas/<slug:company_slug>/detalhes/<uuid:vid>/', views.vacancy_detail, name="vacancy-detail"),
    path('candidaturas/<uuid:vid>/', views.candidacy_list, name="candidacy-list"),

    path('candidaturas/analise/<uuid:vid>/', views.candidacy_analyses, name="candidacy-analyses"),
]