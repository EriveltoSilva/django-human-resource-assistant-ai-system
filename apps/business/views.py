""" Business Views"""

from django.db.models.query import QuerySet
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic
from .forms import RegisterVacancyForm
from .models import Vacancy


def home(request):
    return render(request, "business/home.html")
def candidacy(request):
    return render(request, "business/candidacy.html")

class VacancyDetailView(generic.DetailView):
    """Detail View for a specific vacancy"""
    model = Vacancy
    template_name = "business/vacancy_detail.html"
    context_object_name = "vacancy"
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return Vacancy.objects.get(vid=self.kwargs.get('vid'))
vacancy_detail = VacancyDetailView.as_view()

class VacancyListView(generic.ListView):
    """List View for all vacancies"""
    model = Vacancy
    template_name = "business/vacancy_list.html"
    context_object_name = 'vacancies'

    def get_queryset(self) -> QuerySet[Any]:
        return Vacancy.objects.filter(is_published=True)
vacancy_list = VacancyListView.as_view()

class RegisterVacancyView(View):
    """ Register Vacancy View"""
    template_name = 'business/register_vacancy.html'
    form_class = RegisterVacancyForm

    def get(self, request):
        """register get method to retrieve form"""
        register_vacancy_form = self.form_class(request.session.get("register_vacancy_form_data"))
        return render(request, self.template_name, {"register_vacancy_form":register_vacancy_form})

    def post(self, request):
        """Register post method to save form data"""
        self.request.session["register_vacancy_form_data"] = self.request.POST
        form = self.form_class(self.request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.company = self.request.user
            vacancy.save()
            del request.session['register_vacancy_form_data']
            messages.success(self.request, "Vaga Registada com sucesso!")
            return redirect(reverse('business:vacancy'))
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER') or '')
register_vacancy = RegisterVacancyView.as_view()
