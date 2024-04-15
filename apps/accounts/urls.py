from . import views 
from django.urls import path

app_name = "accounts"
urlpatterns = [
    path('login/', views.login,name="login"),    
    path('logout/', views.logout,name="logout"),    
    path('signup_personal/', views.signup_personal,name="signup-personal"),    
    path('signup_buniness/', views.SignupBusinessView.as_view(),name="signup-business"),    
]
