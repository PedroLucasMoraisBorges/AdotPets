from django.shortcuts import render
from django.views import View
from .models import *
from .forms import *
# Create your views here.

def landingPage(request):
    return render(request, 'landingPage.html')