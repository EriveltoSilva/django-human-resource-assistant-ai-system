from . import views 
from django.urls import path

app_name = "accounts"
urlpatterns = [
    path('login/', views.LoginView.as_view(),name="login"),    
    path('logout/', views.LogoutView.as_view(),name="logout"),    
    path('signup_personal/', views.signup_personal,name="signup-personal"),    
    path('signup_buniness/', views.SignupBusinessView.as_view(),name="signup-business"),    
]
