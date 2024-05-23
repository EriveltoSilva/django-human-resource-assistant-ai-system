from . import utils
from django.views import View
from django.urls import reverse
from django.utils.text import slugify
from django.contrib import messages, auth
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from .models import PersonalProfile, CompanyProfile
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, SignupPersonalForm, SignupBusinessForm, PasswordChangeForm, PasswordResetForm
from . import emails
User = get_user_model()



@method_decorator([login_required(login_url='landing_page', redirect_field_name="next"),], name='dispatch')
class AccountController(View):
    def get(self, *args,**kwargs):
        user_type = "personal" if self.request.user.type == 'P' else "business"
        print("---------------------------------------------->")
        print("Middleware".center(25))
        print("---------------------------------------------->")
        return redirect(reverse(f'{user_type}:user-profile', kwargs={'uid':self.request.user.uid}))
account_controller = AccountController.as_view()

class LoginView(View):
    form_class = LoginForm
    template_name = "accounts/login.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request,self.template_name, {"form":form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email= form.cleaned_data.get('email', '')
            user = auth.authenticate(request, email=email, password=form.cleaned_data.get('password', ''))
            if user:
                auth.login(request, user=user)
                messages.success(request, f"Bem-vindo de volta Sr(a).{request.user.get_full_name()}!")
                return redirect(reverse('accounts:controller'))
            messages.error(request, "Ups! Usuário não Encontrado! Verifique por favor as credências!")
        else:
            messages.error(request, "Error validando o formulário!")
        return redirect('accounts:login')
login = LoginView.as_view()
    
@method_decorator(login_required(login_url='landing_page', redirect_field_name='next'), name='dispatch')
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, "Logout com sucesso!")
        return redirect('landing_page')
    
    def post(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, "Logout com sucesso!")
        return redirect('landing_page')
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
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
            user.set_password(user.password)
            user.type = "P"
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
            try:
                emails.send_register_welcome(user, user.email, 'EJZ Tecnologia', '', 
                                            'http://127.0.0.1:8000/accounts/login/', '',
                                            'http://127.0.0.1:8000/accounts/login/', '')
            except Exception as e:
                print("Error sending email", e)

            messages.success(request, "Usuário Registado com sucesso!")
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
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
            user.set_password(user.password)
            user.type = "B"
            user.save() 
            print(form.cleaned_data.get("sector"))
            CompanyProfile.objects.create(
                user=user,
                sector=form.cleaned_data.get("sector"),
                slug = slugify(f"{form.cleaned_data.get("username")}"),
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

class PasswordResetEmailVerifyView(View):
    form_class = PasswordResetForm
    template_name = "accounts/password-reset.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.session.get("password_reset_form_data", None))
        return render(request,self.template_name, {"form":form})

    def post(self, request, *args, **kwargs):
        request.session['password_reset_form_data'] = request.POST
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                user = get_object_or_404(User, email=form.cleaned_data.get('email'))
                user.otp = otp = utils.generate_otp()
                user.save()
                uidb64 = user.id
                link = f'http://localhost:8000/accounts/alterar-palavra-passe?otp={otp}&uidb64={uidb64}'
                print("#"*100)
                print(link)
                print("#"*100)
                try:
                    emails.send_password_reset(user, user.email, 'EJZ Tecnologia', '', link)
                except Exception as e:
                    print("Error sending email for reset password", e)
                    
                del request.session['password_reset_form_data'] 
                messages.success(request, "Enviamos um email de recuperação de palavra-passe para si!")
            except:
                messages.error(request, "Não temos nenhum usuário vinculado a este e-mail")    
        else:
            messages.error(request, "Error validando o formulário!")
        previous_page = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_page or '')
password_reset = PasswordResetEmailVerifyView.as_view()

class PasswordChangeView(View):
    form_class = PasswordChangeForm 
    template_name = "accounts/password-change.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request,self.template_name, {"form":form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.GET.get("uidb64"), otp=request.GET.get("otp"))
            if user:
                user.set_password(form.cleaned_data.get('new_password'))
                user.otp = ""
                user.reset_token = ""
                user.save()
                messages.success(request, "Palavra-passe alterada com sucesso!")   
                return redirect('accounts:login')
        else:
            messages.error(request, "Error validando o formulário!")
        previous_page = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_page or '')    
password_change = PasswordChangeView.as_view()

