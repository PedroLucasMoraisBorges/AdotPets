from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from .models import *
from .forms import *
from auth_user.models import LogEntrada, LogSaida
from auth_user.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorator import *
from django.forms.models import inlineformset_factory
from datetime import date
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
            return render(request, 'adocao/homeOficial.html', context)
        else:
            print("vv")


            
class adicionarPet(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CadastrarPetForm()
        CadastrarPetFormset = inlineformset_factory(Pet, ImagemPet, form=CadastroImagemForm, extra=1) 
        imgForm = CadastrarPetFormset()

        context = {
            'form':form,
            'imgForm':imgForm
        }
        return render(request, 'cadastros/cadastroPet.html', context)
    
    def post(self, request):
        form = CadastrarPetForm(request.POST)
        CadastrarPetFormset = inlineformset_factory(Pet, ImagemPet, form=CadastroImagemForm, extra=1) 
        imgForm = CadastrarPetFormset(request.POST, request.FILES)
        dt_ent = date.today()

        if form.is_valid() and imgForm.is_valid():
            pet = form.save(commit=False)
            pet.fk_user = request.user
            pet.save()

            log_entrada = LogEntrada.objects.create(fk_doador=request.user, raca=pet.raca, sexo=pet.sexo, dt_entrada=dt_ent)

            imgForm.instance = pet
            imgForm.save()

            return redirect('/meus_Pets/')
        else:
            context = {
                'form': form,
                'imgForm': imgForm,
            }

            return render(request, 'cadastros/cadastroPet.html', context)
    

class editarPet(View):
    @method_decorator(login_required)
    def get(self, request, id):
        pet = Pet.objects.get(id=id)
        form = CadastrarPetForm(instance=pet)

        imgForm_factory = inlineformset_factory(Pet, ImagemPet, form=CadastroImagemForm, extra=0)
        imgForm = imgForm_factory(instance=pet)
        context = {
            'form' : form,
            'imgForm' : imgForm,
            'action': reverse('editarPet', args=[id])
        }

        return render(request, 'configs/editarPet.html', context)
    def post(self, request, id):
        pet = Pet.objects.get(id=id)

        form = CadastrarPetForm(request.POST, instance=pet)
        imgForm_factory = inlineformset_factory(Pet, ImagemPet, form=CadastroImagemForm)
        imgForm = imgForm_factory(request.POST, request.FILES, instance=pet)

        if form.is_valid() and imgForm.is_valid():
            pet = form.save()
            imgForm.instance = pet
            imgForm.save()
            return redirect('/meus_Pets/')

class meusPets(View):
    @method_decorator(login_required)
    def get(self, request,):
        pets = []


        for pet in Pet.objects.filter(fk_user = request.user):
            imgs = ImagemPet.objects.filter(fk_pet = pet)
            pets.append(
                {'pet' : pet,
                 'imgs': imgs}
                )

        context = {
            'pets' : pets
        }

        return render(request, 'adocao/pets.html', context)