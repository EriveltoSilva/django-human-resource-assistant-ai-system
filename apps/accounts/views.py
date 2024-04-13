from django.shortcuts import render, redirect
from .forms import LoginForm
from django.views import View 
from django.contrib import messages, auth
from django.urls import reverse

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
                messages.success(request, f"Bem-vindo de Volta!")
                return redirect('home')
            messages.error(request, f"Ups! Usuário não Encontrado! Verifique por favor as credências!")
        else:
            messages.error(request, f"Error validando o formulário!")

        return redirect('accounts:login')
    


