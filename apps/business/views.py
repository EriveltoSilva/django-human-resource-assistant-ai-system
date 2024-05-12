from .models import Vacancy
from django.views import View
from django.shortcuts import render
from django.contrib import messages
from .forms import RegisterVacancyForm

class RegisterVacancyView(View):
    template_name = 'business/register_vacancy.html'
    form_class = RegisterVacancyForm

    def get(self, request, *args, **kwargs):
        register_vacancy_form = self.form_class(request.session.get("register_vacancy_form_data"))
        return render(self.request, self.template_name, {"register_vacancy_form":register_vacancy_form})
    
    def post(self, request, *args, **kwargs):
        self.request.session["register_vacancy_form_data"] = self.request.POST
        form = self.form_class(self.request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.company = self.request.user
            vacancy.save()
            del(request.session['register_vacancy_form_data'])
            messages.success(self.request, "Vaga Registrada com sucesso!")
            
        
            
register_vacancy = RegisterVacancyView.as_view()


def home(request):
    return render(request, "business/home.html")

def vacancy(request):
    return render(request, "business/vacancy.html")

def candidacy(request):
    return render(request, "business/candidacy.html")
