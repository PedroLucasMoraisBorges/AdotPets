from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from .models import *
from .forms import *
from auth_user.models import LogEntry, LogExit
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

class landingPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            if getUserType(request.user) == 'dafaultUser':
                return redirect('/home/')
            else:
                return redirect('/home/')
        else:
            return render(request, 'homeOficial.html')

class homePage(View):
    def get(self, request):
        search = request.GET.get('Search') if request.GET.get('Search') != None else ''

        pets = []

        for pet in getPetsAdot(request, search):
            imgs = ImagePet.objects.filter(fk_pet = pet)
            contacts = getUserContacts(request, pet)
            pets.append(
                {
                    'pet' : pet,
                    'imgs': imgs,
                    'contacts':contacts}
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
        form = RegisterPetForm()
        print(form)
        imgForm_factory = inlineformset_factory(Pet, ImagePet, form=RegisterImgPet, extra=1, max_num=4, min_num=0, validate_min=True) 
        imgForm = imgForm_factory()


        context = {
            'btn':'Cadastrar Pet',
            'User':request.user,
            'form':form,
            'imgForm':imgForm
        }
        return render(request, 'cadastros/cadastroPet.html', context)
    
    def post(self, request):
        form = RegisterPetForm(request.POST)
        imgForm_factory = inlineformset_factory(Pet, ImagePet, form=RegisterImgPet, extra=1, max_num=4, min_num=0, validate_min=True) 
        imgForm = imgForm_factory(request.POST, request.FILES)
        dt_ent = date.today()

        if form.is_valid() and imgForm.is_valid():
            if request.POST.get('identificador') == "adocao":
                pet = form.save(commit=False)
                pet.fk_user = request.user
                pet.save()

                imgForm.instance = pet
                imgForm.save()

                log_entry = LogEntry.objects.create(fk_donor=request.user, breed=pet.breed, sex=pet.sex, dt_entry=dt_ent)
            else:
                pet = form.save(commit=False)
                pet.fk_user = request.user
                pet.save()

                imgForm.instance = pet
                imgForm.save()

                log_entry = LogEntry.objects.create(fk_donor=request.user, breed=pet.breed, sex=pet.sex, dt_entrada=dt_ent)
                lostPets = LostPets.objects.create(fk_pet=pet)


            return redirect('/perfil/')
        else:
            context = {
                'form': form,
                'imgForm': imgForm,
            }

            return render(request, 'cadastros/cadastroPet.html', context)
    

class editPet(View):
    @method_decorator(login_required)
    def get(self, request, id):
        pet = Pet.objects.get(id=id)
        form = RegisterPetForm(instance=pet)

        imgForm_factory = inlineformset_factory(Pet, ImagePet, form=RegisterImgPet, extra=0)
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

        form = RegisterPetForm(request.POST, instance=pet)
        imgForm_factory = inlineformset_factory(Pet, ImagePet, form=RegisterImgPet)
        imgForm = imgForm_factory(request.POST, request.FILES, instance=pet)

        if form.is_valid() and imgForm.is_valid():
            pet = form.save()
            imgForm.instance = pet
            imgForm.save()
            return redirect('/meus_Pets/')

class meuPerfil(View):
    @method_decorator(login_required)
    @method_decorator(defaultUserRequired)
    def get(self, request,):
        search = request.GET.get('Search') if request.GET.get('Search') != None else ''
    
        pets = []
        pets_fav = []

        user = getDefaultUser(request.user)

        for pet in getMyPets(request.user, search):
            imgs = ImagePet.objects.filter(fk_pet = pet)
            pets.append(
                {
                    'pet' : pet,
                    'imgs': imgs}
                )
            
        for favorite in getFavoritePets(request.user, search):
            imgs = ImagePet.objects.filter(fk_pet = favorite.fk_pet)
            pet = favorite.fk_pet
            pets_fav.append(
                {
                    'pet' : pet,
                    'imgs': imgs}
                )
        
        pag = paginator(request, pets)  
        pag_fav = paginator(request, pets_fav)   

        context = {
            'User' : request.user,
            'info':user,
            'pets' : pag['pet_page'],
            'pets_fav' :pag_fav['pet_page'],
            'page' : pag['page'],
            'nextPage' : pag['nextPage'], 
            'prevPage' : pag['prevPage'],
            'pages': pag['pages'],
            'petName' : search,
            'type': 'Meus Pets',
        }
        
        return render(request, 'perfil/perfil.html', context)

class petsPerdidos(View):
    def get(self, request):
        search = request.GET.get('Search') if request.GET.get('Search') != None else ''
    
        pets = []

        
        for lostPet in getLostPets(request, search):
            pet = lostPet.fk_pet
            imgs = ImagePet.objects.filter(fk_pet = pet)
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
                'type': 'Perdidos'
            }
        else:
            context = {
                'pets' : pag['pet_page'],
                'page' : pag['page'],
                'nextPage' : pag['nextPage'], 
                'prevPage' : pag['prevPage'],
                'pages': pag['pages'],
                'petName' : search,
                'type': 'Perdidos'
            }
        
        return render(request, 'perdidos/petsPerdidos.html', context)


class adotarPet(View):
    def get(self, request, petId, doadorId):

        if request.user.is_authenticated:
            donor = User.objects.get(id=doadorId)
            pet = Pet.objects.get(id=petId)
            donee = request.user


            Requests.objects.create(fk_pet=pet, fk_donor=donor, fk_donee=donee)
            return redirect('/home/')
        else:
            return redirect('/login/')
    
class favoritePet(View):
    def get(self, request, petId):
        pet = Pet.objects.get(id=petId)
        donee = request.user

        Favorites.objects.create(fk_pet=pet, fk_donee=donee)
        return redirect('/home/')