from django.shortcuts import render
from django.contrib import messages
from django.views import View, generic
from apps.accounts.models import PersonalProfile
from .forms import PersonalInformationForm, PersonalProfileInformationForm, AcademicFormationForm, ProfissionalFormationForm, ProfissionalExperienceForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Formation, AcademicFormationItem, ProfissionalFormationItem, ProfissionalExperienceItem, ProfissionalExperience

from django.http import HttpResponseRedirect

def home(request):
    return render(request, "personal/home.html")


@method_decorator([login_required(login_url="accounts:login", redirect_field_name="next"),], name='dispatch')
class CareerView(View):
    template_name = "personal/career.html"
    def get(self, request, *args, **kwargs):
        formation, created = Formation.objects.get_or_create(user=request.user)
        experience, exe_created = ProfissionalExperience.objects.get_or_create(user=request.user)

        personal_info_form = PersonalInformationForm(instance=request.user)
        personal_profile_form = PersonalProfileInformationForm(request.session.get('personal_info_form_data'), instance=request.user.personal_profile)
        
        personal_academic_formation_form = AcademicFormationForm(request.session.get('personal_academic_formation_form_data', None))
        personal_profissional_formation_form = ProfissionalFormationForm(request.session.get('personal_profissional_formation_form_data', None))

        personal_profissional_experience_form = ProfissionalExperienceForm(request.session.get('personal_profissional_experience_form_data', None))

        acad_formation_items = AcademicFormationItem.objects.filter(formation=formation)
        prof_formation_items = ProfissionalFormationItem.objects.filter(formation=formation)

        prof_experience_items = ProfissionalExperienceItem.objects.filter(profissional_experience=experience)


        return render(self.request, self.template_name, {
            "personal_info_form":personal_info_form,
            "personal_profile_form":personal_profile_form,
            "personal_academic_formation_form":personal_academic_formation_form,
            "personal_profissional_formation_form":personal_profissional_formation_form,

            "personal_profissional_experience_form":personal_profissional_experience_form,

            "acad_formation_items":acad_formation_items,
            "prof_formation_items":prof_formation_items,          
            "prof_experience_items":prof_experience_items,

            })
career = CareerView.as_view()



@method_decorator([login_required(login_url="accounts:login", redirect_field_name="next"),], name='dispatch')
class AddProfissionalExperienceItem(View):
    form_class = ProfissionalExperienceForm

    def post(self, request, *args, **kwargs):
        experience, created = ProfissionalExperience.objects.get_or_create(user=request.user)
        request.session['personal_profissional_experience_form_data'] = request.POST
        form = self.form_class(request.session['personal_profissional_experience_form_data'])
        if form.is_valid():
            experience_item = form.save(commit=False)
            experience_item.profissional_experience = experience
            experience_item.save()
            messages.success(request, "Experiência Profissional Adicionada com sucesso!")
            del(request.session['personal_profissional_experience_form_data'])
        else:
            messages.error(request, "Erro: Preencha todos os campos!")
            print(form.errors)

        previous_page = self.request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_page or '')
add_profissional_experience = AddProfissionalExperienceItem.as_view()

@method_decorator([login_required(login_url="accounts:login", redirect_field_name="next"),], name='dispatch')
class DeleteProfissionalFormationItem(View):
    def post(self, *args, **kwargs):
        formation = ProfissionalFormationItem.objects.get(aid=self.kwargs['id'])
        formation.delete()
        messages.success(self.request,"Formação eliminada com sucesso!")
        previous_page = self.request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_page or '')
delete_profissional_formation = DeleteProfissionalFormationItem.as_view()

@method_decorator([login_required(login_url="accounts:login", redirect_field_name="next"),], name='dispatch')
class DeleteAcademicFormationItem(View):
    def post(self, *args, **kwargs):
        formation = AcademicFormationItem.objects.get(aid=self.kwargs['id'])
        formation.delete()
        messages.success(self.request,"Formação eliminada com sucesso!")
        previous_page = self.request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_page or '')
delete_academic_formation = DeleteAcademicFormationItem.as_view()


@method_decorator([login_required(login_url="accounts:login", redirect_field_name="next"),], name='dispatch')
class AddProfissionalFormationItem(View):
    form_class = ProfissionalFormationForm

    def post(self, request, *args, **kwargs):
        formation, created = Formation.objects.get_or_create(user=request.user)
        request.session['personal_profissional_formation_form_data'] = request.POST
        form = self.form_class(request.session['personal_profissional_formation_form_data'])
        if form.is_valid():
            formation_item = form.save(commit=False)
            formation_item.formation = formation
            formation_item.save()
            messages.success(request, "Formação Profissional Adicionada com sucesso!")
            del(request.session['personal_profissional_formation_form_data'])
        else:
            messages.error(request, "Erro: Preencha todos os campos!")
            print(form.errors)

        previous_page = self.request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_page or '')
add_profissional_formation = AddProfissionalFormationItem.as_view()


@method_decorator([login_required(login_url="accounts:login", redirect_field_name="next"),], name='dispatch')
class AddAcademicFormationItem(View):
    form_class = AcademicFormationForm

    def post(self, request, *args, **kwargs):
        formation, created = Formation.objects.get_or_create(user=request.user)

        request.session['personal_academic_formation_form_data'] = request.POST
        form = self.form_class(request.session['personal_academic_formation_form_data'])
        if form.is_valid():
            formation_item = form.save(commit=False)
            formation_item.formation = formation
            formation_item.save()
            messages.success(request, "Formação Adicionada com sucesso!")
            del(request.session['personal_academic_formation_form_data'])
        else:
            messages.error(request, "Erro: Preencha todos os campos!")
            print(form.errors)

        previous_page = self.request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_page or '')
add_academic_formation = AddAcademicFormationItem.as_view()


@method_decorator([login_required(login_url="accounts:login", redirect_field_name="next"),], name='dispatch')
class ProfileUpdateView(View):
    form_class = PersonalProfileInformationForm

    def post(self, request, *args, **kwargs):
        profile = request.user.personal_profile
        request.session['personal_info_form_data'] = request.POST
        form = self.form_class(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            # user_profile.save()
            messages.success(request, "Perfil Editado com sucesso!")
            del(request.session['personal_info_form_data'])
        else:
            messages.error(request, "Erro: Preecha todos os campos!")
            print(form.errors)
        previous_page = self.request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_page or '')
profile_update = ProfileUpdateView.as_view()
