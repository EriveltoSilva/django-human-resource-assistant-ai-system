from django.views import View 
from django.urls import reverse
from django.utils.text import slugify
from django.contrib import messages, auth
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from .models import PersonalProfile, CompanyProfile
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, SignupPersonalForm, SignupBusinessForm

User = get_user_model()

class LoginView(View):
    form_class = LoginForm
    template_name = "accounts/login.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request,self.template_name, {"form":form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = auth.authenticate(
                request,
                username=form.cleaned_data.get('username', ''), 
                password=form.cleaned_data.get('password', '')
            )
            if user:
                auth.login(request, user=user)
                messages.success(request, f"Bem-vindo de volta Sr(a).{request.user.get_full_name()}!")
                return redirect('landing_page')
            messages.error(request, "Ups! Usuário não Encontrado! Verifique por favor as credências!")
        else:
            messages.error(request, "Error validando o formulário!")
        return redirect('accounts:login')
login = LoginView.as_view()
    
@method_decorator(login_required(login_url="accounts:login", redirect_field_name='next'), name='dispatch')
class LogoutView(View):
    # @method_decorator(login_required(login_url="accounts:login", redirect_field_name='next'))
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.error(request, "Logout com sucesso!")
        return redirect('accounts:login')
    
    # def post(self, request, *args, **kwargs):
    #     auth.logout(request)
    #     messages.error(request, "Logout com sucesso!")
    #     return redirect('accounts:login')
logout = LogoutView.as_view()
    
class SignupPersonalView(View):
    form_class = SignupPersonalForm
    template_name = "accounts/signup-personal.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.session.get("signup_personal_form_data", None))
        return render(request, self.template_name, {"form":form})
    
    def post(self, request, *args, **kwargs):
        request.session['signup_personal_form_data'] = request.POST
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save() 
            PersonalProfile.objects.create(
                user=user,
                slug = slugify(f"{user.username}"),
                bi = form.cleaned_data.get("bi"),
                gender = form.cleaned_data.get("gender"),
                phone = form.cleaned_data.get("phone"),
                address = form.cleaned_data.get("address"),
                birthday = form.cleaned_data.get("birthday")
            )
            messages.success(request, "Usuário Registrado com sucesso!")
            del(request.session['signup_personal_form_data'])
            return redirect("accounts:login")
        print(form.errors)
        return redirect("accounts:signup-personal")
signup_personal = SignupPersonalView.as_view()

class SignupBusinessView(View):
    form_class = SignupBusinessForm
    template_name = "accounts/signup-business.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.session.get("signup_business_form_data", None))
        return render(request, self.template_name, {"form":form})
    
    def post(self, request, *args, **kwargs):
        request.session['signup_business_form_data'] = request.POST
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save() 
            print(form.cleaned_data.get("sector"))
            CompanyProfile.objects.create(
                user=user,
                sector=form.cleaned_data.get("sector"),
                slug = slugify(f"{user.username}"),
                nif = form.cleaned_data.get("nif"),
                phone = form.cleaned_data.get("phone"),
                address = form.cleaned_data.get("address"),
                website = form.cleaned_data.get("website")
            )
            messages.success(request, "Usuário Registrado com sucesso!")
            del(request.session['signup_business_form_data'])
            return redirect("accounts:login")
        print(form.errors)
        return redirect("accounts:signup-business")
signup_business = SignupBusinessView.as_view()

###############################################################################################
# @require_POST
# @login_required(login_url="accounts:login", redirect_field_name="next")
# def delete_user(request, id):
#     user = get_object_or_404(User, pk=id)
#     user.delete()
#     messages.success(request, "Usuário eliminado com sucesso")
#     return redirect(reverse('accounts:list'))


###############################################################################################
# @require_POST
# @login_required(login_url="accounts:login", redirect_field_name="next")
# def list_accounts(request):
#     list_accounts = User.objects.all()
#     paginator = Paginator(list_accounts, 10)
#     page = request.GET.get('page')
#     accounts = paginator.get_page(page)
#     # page = utils.get_sub_nav_headers("Listagem","Usuários", "Usuários registrados")
#     return render(request, "accounts/list.html",{"accounts":accounts, "page":page})

###############################################################################################
# @login_required(login_url="accounts:login", redirect_field_name="next")
# def edit_view(request, id):
#     user = get_object_or_404(User, pk=id)
#     if request.session.get("edit_form_data", None):
#         form = EditUserForm(request.session.get("edit_form_data", None), instance=user)
#     else:
#         form = EditUserForm(instance=user)
#     return render(request, "accounts/edit.html", {"form": form, "user":user})


###############################################################################################
# @login_required(login_url="accounts:login", redirect_field_name="next")
# def edit_user(request, id):
#     if request.method != 'POST':
#         raise Http404()
    
#     user = get_object_or_404(User, pk=id)
#     request.session['edit_form_data'] = request.POST
#     form = EditUserForm(request.POST, instance=user)
#     if form.is_valid():
#        form_user = form.save(commit=False)
#        form_user.set_password(form_user.password)
#        form_user.save() 
#        messages.success(request, "Usuário Editado com sucesso!")
#        del(request.session['edit_form_data'])
#        return redirect(reverse("accounts:list"))
#     print(form.errors)
#     messages.error(request, "Formulário de Edição Inválido!")
#     return redirect(reverse("accounts:edit-view", args=(user.id,)))

