from .forms import LoginForm, SignupPersonalForm
from django.views import View 
from django.urls import reverse
from django.contrib import messages, auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, "accounts/login.html", {"form":form})
    
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
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
    

# ###############################################################################################
# def register_view(request):
#     form = SignupPersonalForm(request.session.get("signup_personal_form_data", None))
#     return render(request, "accounts/signup-personal.html", {"form": form})

# ###############################################################################################
# def register_create(request):    
#     request.session['signup_personal_form_data'] = request.POST
#     form = SignupPersonalForm(request.POST)
#     if form.is_valid():
#        user = form.save(commit=False)
#        user.set_password(user.password)
#        user.save() 
#        messages.success(request, "Usuário Registrado com sucesso!")
#        del(request.session['signup_personal_form_data'])
#     return redirect("accounts:signup-personal")
 

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
            messages.success(request, "Usuário Registrado com sucesso!")
            del(request.session['signup_personal_form_data'])
            return redirect("accounts:login")
        print(form.errors)
        return redirect("accounts:signup-personal")

signup_personal = SignupPersonalView.as_view()


class SignupBusinessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "accounts/signup-business.html")

