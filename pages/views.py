from django.shortcuts import render
from django.views import View
from .models import *
from .forms import *
# Create your views here.

def landingPage(request):
    return render(request, 'landingPage.html')

class homePage(View):
    def get(self, request):
        return render(request, 'adocao/home.html')