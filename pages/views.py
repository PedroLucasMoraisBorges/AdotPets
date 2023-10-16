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
from django.core.paginator import Paginator
from django.db.models import Q
from .utilits import *
# Create your views here.

def paginator(request, pets):
    page = request.GET.get('page') if request.GET.get('page') != None else 1
    p = Paginator(pets, 8)
    pages = p.num_pages

    if int(page) < 1 or int(page) > int(pages):
        page = 1

    pet_page = p.get_page(page)
    nextPage = int(page) + 1
    prevPage = int(page) - 1
    return {
        'page' : int(page),
        'pet_page':pet_page,
        'nextPage':nextPage,
        'prevPage':prevPage,
        'pages':int(pages)
    }

def landingPage(request):
    return render(request, 'homeOficial.html')

class homePage(View):
    #@method_decorator(login_required)
    def get(self, request):
        search = request.GET.get('Search') if request.GET.get('Search') != None else ''

        pets = []

        for pet in getPetsAdot(request.user, search):
            imgs = ImagemPet.objects.filter(fk_pet = pet)
            pets.append(
                {
                    'pet' : pet,
                    'imgs': imgs}
                )
            
        pag = paginator(request, pets)
        

        if request.user.is_authenticated:
            context = {
            'User' : request.user,
            'pets' : pag['pet_page'],
            'page' : pag['page'],
            'nextPage' : pag['nextPage'], 
            'prevPage' : pag['prevPage'],
            'pages': pag['pages'],
            'petName' : search,
            'type': 'Adoção'
        }
        else:
            context = {
            'pets' : pag['pet_page'],
            'page' : pag['page'],
            'nextPage' : pag['nextPage'], 
            'prevPage' : pag['prevPage'],
            'pages': pag['pages'],
            'petName' : search,
            'type': 'Adoção'
        }
        return render(request, 'adocao/animais.html', context)


            
class adicionarPet(View):
    @method_decorator(login_required)
    def get(self, request):
        pet = request.GET.get('id')
        form = CadastrarPetForm()
        CadastrarPetFormset = inlineformset_factory(Pet, ImagemPet, form=CadastroImagemForm, extra=1, max_num=4, min_num=0, validate_min=True) 
        imgForm = CadastrarPetFormset()


        context = {
            'btn':'Cadastrar Pet',
            'User':request.user,
            'form':form,
            'imgForm':imgForm
        }
        return render(request, 'cadastros/cadastroPet.html', context)
    
    def post(self, request):
        form = CadastrarPetForm(request.POST)
        CadastrarPetFormset = inlineformset_factory(Pet, ImagemPet, form=CadastroImagemForm, extra=1, max_num=4, min_num=0, validate_min=True) 
        imgForm = CadastrarPetFormset(request.POST, request.FILES)
        dt_ent = date.today()

        if form.is_valid() and imgForm.is_valid():
            if request.POST.get('identificador') == "adocao":
                pet = form.save(commit=False)
                pet.fk_user = request.user
                pet.save()

                imgForm.instance = pet
                imgForm.save()

                log_entrada = LogEntrada.objects.create(fk_doador=request.user, raca=pet.raca, sexo=pet.sexo, dt_entrada=dt_ent)
            else:
                pet = form.save(commit=False)
                pet.fk_user = request.user
                pet.save()

                imgForm.instance = pet
                imgForm.save()

                log_entrada = LogEntrada.objects.create(fk_doador=request.user, raca=pet.raca, sexo=pet.sexo, dt_entrada=dt_ent)
                animaisPerdidos = AnimaisPerdidos.objects.create(fk_pet=pet)


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
            'btn': "Editar Pet",
            'User' : request.user,
            'form' : form,
            'imgForm' : imgForm,
            'action': reverse('editarPet', args=[id])
        }

        return render(request, 'cadastros/cadastroPet.html', context)
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
        search = request.GET.get('Search') if request.GET.get('Search') != None else ''
    
        pets = []


        for pet in getMyPets(request.user, search):
            imgs = ImagemPet.objects.filter(fk_pet = pet)
            pets.append(
                {
                    'pet' : pet,
                    'imgs': imgs}
                )
        
        pag = paginator(request, pets)
        
        context = {
            'User' : request.user,
            'pets' : pag['pet_page'],
            'page' : pag['page'],
            'nextPage' : pag['nextPage'], 
            'prevPage' : pag['prevPage'],
            'pages': pag['pages'],
            'petName' : search,
            'type': 'Meus Pets'
        }
        
        return render(request, 'adocao/pets.html', context)

class petsPerdidos(View):
    @method_decorator(login_required)
    def get(self, request):
        search = request.GET.get('Search') if request.GET.get('Search') != None else ''
    
        pets = []


        for pet in getLostPets(request.user, search):
            imgs = ImagemPet.objects.filter(fk_pet = pet.fk_pet)
            pets.append(
                {
                    'pet' : pet,
                    'imgs': imgs}
                )
        
        pag = paginator(request, pets)
        
        context = {
            'User' : request.user,
            'pets' : pag['pet_page'],
            'page' : pag['page'],
            'nextPage' : pag['nextPage'], 
            'prevPage' : pag['prevPage'],
            'pages': pag['pages'],
            'petName' : search,
            'type': 'Meus Pets'
        }
        
        return render(request, 'adocao/pets.html', context)


class adotarPet(View):
    def get(self, request, petId, doadorId):
        doador = User.objects.get(id=doadorId)
        pet = Pet.objects.get(id=petId)
        donatario = request.user

        print(doador)

        Requisicoes.objects.create(fk_pet=pet, fk_doador=doador, fk_donatario=donatario)
        return redirect('/home/')
    
class favoritarPet(View):
    def get(self, request, petId):
        pet = Pet.objects.get(id=petId)
        donatario = request.user

        Favoritos.objects.create(fk_pet=pet, fk_donatario=donatario)
        return redirect('/home/')