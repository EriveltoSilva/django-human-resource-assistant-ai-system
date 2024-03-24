from . import views 
from django.urls import path

app_name="users"
urlpatterns = [
    path('usuarios/registrar', views.register_view, name='register-view'),
    path('usuarios/registrar/registrar-usuario', views.register_create, name='register-create'),
    path('usuarios/login/', views.login_view, name='login'),
    path('usuarios/fazer-login/', views.login_create, name='login-create'),
    path('usuarion/logout/', views.logout, name='logout'),
    path('usuarios/listagem/', views.list_users, name='list'),
    path('usuarios/editar/<int:id>/', views.edit_view, name='edit-view'),
    path('usuarios/editar/registrar-edicao/<int:id>/', views.edit_user, name='edit-create'),
    path('usuarios/deletar/<int:id>/', views.delete_user, name='delete'),

    path('usuarios/editar/imagem/<int:id>/', views.edit_user_image, name='edit-image'),
]
