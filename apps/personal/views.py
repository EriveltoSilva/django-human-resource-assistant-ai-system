from django.shortcuts import render
from django.contrib import messages
from django.views import View, generic
from apps.accounts.models import PersonalProfile
from .forms import PersonalInformationForm, PersonalProfileInformationForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect

def home(request):
    return render(request, "personal/home.html")

class CareerView(View):
    template_name = "personal/career.html"
    form_class = PersonalInformationForm
    def get(self, request, *args, **kwargs):
        personal_info_form = self.form_class(instance=request.user)
        personal_profile_form = PersonalProfileInformationForm(request.session.get('personal_info_form_data'), instance=request.user.personal_profile)
        return render(self.request, self.template_name, {
            "personal_info_form":personal_info_form,
            "personal_profile_form":personal_profile_form,

            })
    
@method_decorator([login_required(login_url="users:login", redirect_field_name="next"),], name='dispatch')
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
career = CareerView.as_view()