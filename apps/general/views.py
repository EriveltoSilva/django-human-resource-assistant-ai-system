from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

def home(request):
    return HttpResponse("<h1>Hello</h1>")

class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "landing-page.html")