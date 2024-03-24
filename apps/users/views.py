from apps.general import utils
from .forms import LoginForm
from django.http import Http404
from .forms import RegisterForm
from .forms import EditUserForm
from django.contrib import auth
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse



@login_required(login_url="users:login", redirect_field_name="next")
def delete_user(request, id):
    if request.method != 'POST':
        raise Http404()
    user = get_object_or_404(User, pk=id)
    user.delete()
    messages.success(request, "Usuário eliminado com sucesso")
    return redirect(reverse('users:list'))


###############################################################################################
@login_required(login_url="users:login", redirect_field_name="next")
def list_users(request):
    # list_users = User.objects.filter(profile__isnull=False).order_by('profile__area')
    list_users = User.objects.all()
    paginator = Paginator(list_users, 10)
    page = request.GET.get('page')
    users = paginator.get_page(page)
    page = utils.get_sub_nav_headers("Listagem","Usuários", "Usuários registrados")
    return render(request, "users/list.html",{"users":users, "page":page})

###############################################################################################
@login_required(login_url="users:login", redirect_field_name="next")
def edit_view(request, id):
    user = get_object_or_404(User, pk=id)
    if request.session.get("edit_form_data", None):
        form = EditUserForm(request.session.get("edit_form_data", None), instance=user)
    else:
        form = EditUserForm(instance=user)
    return render(request, "users/edit.html", {"form": form, "user":user})


###############################################################################################
@login_required(login_url="users:login", redirect_field_name="next")
def edit_user(request, id):
    if request.method != 'POST':
        raise Http404()
    
    user = get_object_or_404(User, pk=id)
    request.session['edit_form_data'] = request.POST
    form = EditUserForm(request.POST, instance=user)
    if form.is_valid():
       form_user = form.save(commit=False)
       form_user.set_password(form_user.password)
       form_user.save() 
       messages.success(request, "Usuário Editado com sucesso!")
       del(request.session['edit_form_data'])
       return redirect(reverse("users:list"))
    print(form.errors)
    messages.error(request, "Formulário de Edição Inválido!")
    return redirect(reverse("users:edit-view", args=(user.id,)))



###############################################################################################
@login_required(login_url="users:login", redirect_field_name="next")
def register_view(request):
    form = RegisterForm(request.session.get("register_form_data", None))
    return render(request, "users/register.html", {"form": form})

###############################################################################################
@login_required(login_url="users:login", redirect_field_name="next")
def register_create(request):
    if not request.method == 'POST':
        raise Http404()
    
    request.session['register_form_data'] = request.POST
    form = RegisterForm(request.POST)
    if form.is_valid():
       user = form.save(commit=False)
       user.set_password(user.password)
       user.save() 
       messages.success(request, "Usuário Registrado com sucesso!")
       del(request.session['register_form_data'])
    return redirect("users:register-view")
 



###############################################################################################
@login_required(login_url="users:login", redirect_field_name="next")
def logout(request):
    if not request.method == 'POST':
        raise Http404()
    auth.logout(request)
    messages.error(request, "Logout com sucesso!")
    return redirect('users:login')

def login_view(request):
    form = LoginForm()
    return render(request, "users/login.html",{"form":form})

def login_create(request):
    if not request.method == 'POST':
        raise Http404()
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

    return redirect('users:login')





def read_user(request):
    ...

def edit_user_image(request):
    ...
def get_users(request):
    ...
