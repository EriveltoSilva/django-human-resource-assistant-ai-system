""" Business Views"""
from django.db.models import Count
from django.views import View
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Vacancy, Candidate
from .forms import RegisterVacancyForm, VacancySkillForm
from .forms import VacancyResponsibilityForm, VacancyBenefitForm



def home(request):
    return render(request, "business/home.html")

@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next")],name='dispatch')
class CandidacyListView(View):
    """List View for all candidate applied in a vacancy"""
    model = Candidate
    template_name = "business/candidacy_list.html"
    context_object_name = 'candidates'
    paginate_by = 5
    def get(self, request, *args, **kwargs):
        """get all  candidates applied to the vacancy"""
        vacancy = Vacancy.objects.get(vid=self.kwargs.get('vid'))
        list_candidates = Candidate.objects.filter(vacancy=vacancy)
        total_candidates = len(list_candidates)
        paginator = Paginator(list_candidates,5)
        candidates = paginator.get_page(self.request.GET.get('page'))

        return render(self.request, self.template_name, {'candidates': candidates, "vacancy": vacancy, "total_candidates":total_candidates})

candidacy_list = CandidacyListView.as_view()

class _BasicVacancyEditViewModel(View):
    template_name = "business/vacancy_edit.html"
    form_class = RegisterVacancyForm

    def get_instance(self) -> Vacancy:
        """get the current edit instance of vacancy 
        Returns:
            Vacancy: current vacancy
        """
        vacancy = Vacancy.objects.get(vid=self.kwargs.get("vid"))
        return vacancy

    def get(self, *args, **kwargs):
        """retrieve edit page with forms"""
        vacancy = self.get_instance()
        vacancy_information_form = self.form_class(self.request.session.get("vacancy_basic_form_data", None),instance=vacancy)
        vacancy_skills_form = VacancySkillForm(self.request.session.get("vacancy_skills_form_data", None))
        vacancy_responsibilities_form = VacancySkillForm(self.request.session.get("vacancy_responsibility_form_data", None))
        vacancy_benefits_form = VacancySkillForm(self.request.session.get("vacancy_benefits_form_data", None))
        return render(self.request, self.template_name, {
            "vacancy":vacancy, 
            "vacancy_information_form":vacancy_information_form,
            "vacancy_skills_form":vacancy_skills_form,
            "vacancy_responsibilities_form":vacancy_responsibilities_form,
            "vacancy_benefits_form":vacancy_benefits_form
        })

@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next")],name='dispatch')
class VacancyBenefitsViewEdit(_BasicVacancyEditViewModel):
    """edit vacancy skills view"""
    form_class = VacancyBenefitForm

    def post(self,*args, **kwargs):
        """ save benefits"""
        self.request.session['vacancy_benefits_form_data'] = self.request.POST
        form = self.form_class(self.request.POST)
        if form.is_valid():
            benefit = form.save(commit=False)
            benefit.vacancy = self.get_instance()
            benefit.save()
            messages.success(self.request, "Benefício salvo com sucesso!")
            del self.request.session['vacancy_benefits_form_data']
        print(form.errors)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER') or '')
add_vacancy_benefits = VacancyBenefitsViewEdit.as_view()

@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next")],name='dispatch')
class VacancyResponsibilityViewEdit(_BasicVacancyEditViewModel):
    """edit vacancy responsibility view"""
    form_class = VacancyResponsibilityForm

    def post(self,*args, **kwargs):
        """ save responsibility"""
        self.request.session['vacancy_responsibility_form_data'] = self.request.POST
        form = self.form_class(self.request.POST)
        if form.is_valid():
            responsibility = form.save(commit=False)
            responsibility.vacancy = self.get_instance()
            responsibility.save()
            messages.success(self.request, "Responsabilidade salva com sucesso!")
            del self.request.session['vacancy_responsibility_form_data']
        print(form.errors)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER') or '')
add_vacancy_responsibilities = VacancyResponsibilityViewEdit.as_view()

@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next")],name='dispatch')
class VacancySkillSViewEdit(_BasicVacancyEditViewModel):
    """edit vacancy skills view"""
    form_class = VacancySkillForm

    def post(self,*args, **kwargs):
        """ save skills"""
        self.request.session['vacancy_skills_form_data'] = self.request.POST
        form = self.form_class(self.request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.vacancy = self.get_instance()
            skill.save()
            messages.success(self.request, "Requisito salvo com sucesso!")
            del self.request.session['vacancy_skills_form_data']
        print(form.errors)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER') or '')
add_vacancy_skills = VacancySkillSViewEdit.as_view()

@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next"),], name='dispatch')
class EditVacancyView(_BasicVacancyEditViewModel):
    """edit vacancy view"""
    def post(self,request, *args, **kwargs):
        """ save vacancy edit"""
        request.session['vacancy_basic_form_data'] = request.POST
        form = self.form_class(request.POST, instance=self.get_instance())
        if form.is_valid():
            form.save()
            messages.success(request, "Vaga Editada com sucesso!")
            del request.session['vacancy_basic_form_data']
        print(form.errors)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER') or '')
edit_vacancy = EditVacancyView.as_view()

@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next")],name='dispatch')
class DeleteVacancyView(View):
    """delete vacancy view"""
    def post(self, *args, **kwargs):
        """post method for delete processing request
        Returns:
            http redirect response: redirect url view
        """
        vacancy = Vacancy.objects.get(vid=self.kwargs.get('vid'))
        vacancy.delete()
        messages.success(self.request, "Vaga eliminada com sucesso!")
        return redirect(reverse('business:vacancy-list'))
delete_vacancy = DeleteVacancyView.as_view()

@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next")],name='dispatch')
class VacancyDetailView(generic.DetailView):
    """Detail View for a specific vacancy"""
    model = Vacancy
    template_name = "business/vacancy_detail.html"
    context_object_name = "vacancy"

    def get_object(self, *args, **kwargs):
        return Vacancy.objects.get(vid=self.kwargs.get('vid'))
vacancy_detail = VacancyDetailView.as_view()

@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next")],name='dispatch')
class VacancyListView(generic.ListView):
    """List View for all vacancies"""
    model = Vacancy
    template_name = "business/vacancy_list.html"
    context_object_name = 'vacancies'

    def get_queryset(self):
        """get all my published vacancies annotated with the number of candidates"""
        return Vacancy.objects.filter(is_published=True, company=self.request.user).annotate(
            candidate_count=Count('candidate')
        )
vacancy_list = VacancyListView.as_view()

@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next")],name='dispatch')
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
