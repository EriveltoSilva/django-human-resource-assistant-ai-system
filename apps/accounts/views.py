from .forms import LoginForm
from django.views import View 
from django.urls import reverse
from django.contrib import messages, auth
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
                return redirect('home')
            messages.error(request, f"Ups! Usuário não Encontrado! Verifique por favor as credências!")
        else:
            messages.error(request, f"Error validando o formulário!")

        return redirect('accounts:login')
    

#Decora o metodo dispatch(2º metodo a ser chamado quando a class é inicializada) da class com login_required
@method_decorator(
    login_required(login_url="accounts:login", redirect_field_name='next'), 
    name='dispatch'
)
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
    
