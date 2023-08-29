from django.shortcuts import render
from django.views import View
from .models import *
from .forms import *
from auth_user.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorator import *
from PIL import Image
# Create your views here.

def landingPage(request):
    return render(request, 'landingPage.html')


class homePage(View):
    @method_decorator(login_required)
    def get(self, request):
        if request.user.is_authenticated:
            defaultUser = DefaultUser.objects.get(fk_user = request.user)
            context = {
                'defaultUser' : defaultUser
            }
            return render(request, 'adocao/home.html', context)
        else:
            print("vv")

def adicionarPet(request):
    if request.POST:
        form = cadastrarPet(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            form.save()
    return render(request, 'cadastros/cadastroPet.html', {'form' : cadastrarPet(request.POST, request.FILES)})