from django.urls import path
from . import views
app_name= "business"

urlpatterns = [
    path('home/', views.home, name="home"),
    path('vagas/', views.vacancy_list, name="vacancy_list"),
    path('vagas/<slug:company_slug>/detalhes/<uuid:vid>/', views.vacancy_detail, name="vacancy_detail"),
    path('nova-vaga/', views.register_vacancy, name="register-vacancy"),
    path('candidaturas/', views.candidacy, name="candidacy"),
]