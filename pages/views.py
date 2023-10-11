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
# Create your views here.

def landingPage(request):
    return render(request, 'homeOficial.html')

class homePage(View):
    #@method_decorator(login_required)
    def get(self, request):
        search = request.GET.get('search')
        
        if search:
            pet_list = Pet.objects.filter(raca__icontains = search)
        else:
            pet_list = Pet.objects.all()
        pets = []
        for pet in pet_list:
            imgs = ImagemPet.objects.filter(fk_pet = pet)

            pets.append(
                {
                    'pet' : pet,
                    'imgs': imgs,
                }
            )
        if request.user.is_authenticated:
            context = {
                'User' : request.user,
                'pets' : pets
            }
        else:
            context = {
                'pets' : pets
            }
        return render(request, 'adocao/animais.html', context)


            
class adicionarPet(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CadastrarPetForm()
        CadastrarPetFormset = inlineformset_factory(Pet, ImagemPet, form=CadastroImagemForm, extra=1, max_num=4, min_num=0, validate_min=True) 
        imgForm = CadastrarPetFormset()

        context = {
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
            'User' : request.user,
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
        page = request.GET.get('page') if request.GET.get('page') != None else 1
        petName = request.GET.get('petName') if request.GET.get('petName') != None else ''
    
        pets = []


        for pet in reversed(Pet.objects.filter(fk_user = request.user).filter(nome__istartswith=petName)):
            imgs = ImagemPet.objects.filter(fk_pet = pet)
            pets.append(
                {
                    'pet' : pet,
                    'imgs': imgs}
                )


        p = Paginator(pets, 8)
        pages = p.num_pages

        if int(page) < 1 or int(page) > int(pages):
            page = 1

        pet_page = p.get_page(page)
        nextPage = int(page) + 1
        prevPage = int(page) - 1

        context = {
            'pets' : pet_page,
            'page' : int(page),
            'nextPage' : nextPage, 
            'prevPage' : prevPage,
            'pages': int(pages),
            'petName' : petName,
        }
        
        return render(request, 'adocao/pets.html', context)

class petsPerdidos(View):
    @method_decorator(login_required)
    def get(self, request):
        search = request.GET.get('search')
        if search:
            pet_list = AnimaisPerdidos.objects.filter(fk_pet__raca__contains = search)
        else:
            pet_list = AnimaisPerdidos.objects.all()
        
        pets = []
        for petPerdido in pet_list:
            imgs = ImagemPet.objects.filter(fk_pet = petPerdido.fk_pet)
            pets.append(
                {
                    'pet'  : petPerdido.fk_pet,
                    'imgs' : imgs, 
                }
            )
        context = {
            'User': request.user,
            'pets' : pets
        }
        return render(request, 'perdidos/petsPerdidos.html', context)
