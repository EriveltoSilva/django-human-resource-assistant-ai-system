from django.urls import reverse
from django.http import HttpResponse
from django.views import View, generic
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required



    

class LandingPageView(generic.TemplateView):
    template_name = 'landing-page.html'