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
from auth_user.forms import *
from django.core.mail import send_mail

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
        if request.user.is_authenticated == False:
            return render(request, 'homeOficial.html')
        else:
            return redirecionar_usuario(request.user)
            

class homePage(View):
    def get(self, request):
        search = request.GET.get('Search') if request.GET.get('Search') != None else ''

        pets = []

        for pet in getPetsAdot(request, search):
            imgs = ImagePet.objects.filter(fk_pet = pet)
            contacts = getUserContacts(request, pet)
            favoritePet = getTestFavoritePets(pet, request.user)
            pets.append(
                {
                    'pet' : pet,
                    'imgs': imgs,
                    'contacts':contacts,
                    'type': "adot",
                    'favoritePet':favoritePet}
                )
            
        pag = paginator(request, pets)
        

        if request.user.is_authenticated:
            context = {
            'info':getDefaultUser(request.user),
            'pets' : pag['pet_page'],
            'page' : pag['page'],
            'nextPage' : pag['nextPage'], 
            'prevPage' : pag['prevPage'],
            'pages': pag['pages'],
            'petName' : search,
        }
        else:
            context = {
            'pets' : pag['pet_page'],
            'page' : pag['page'],
            'nextPage' : pag['nextPage'], 
            'prevPage' : pag['prevPage'],
            'pages': pag['pages'],
            'petName' : search,
        }
        return render(request, 'adocao/animais.html', context)

    def post(self, request):
        if request.method == 'POST' and 'sendRequestButton' in request.POST:
            
            if request.user.is_authenticated:
                donor = User.objects.get(id=request.POST.get('id_user'))
                pet = Pet.objects.get(id=request.POST.get('id_pet'))
                text = request.POST.get('requestText')
                donee = request.user

                Requests.objects.create(fk_pet=pet, fk_donor=donor, fk_donee=donee, requestText=text)

                message = donee.username + " enviou uma solitação para a adoção do seu pet " + pet.name + "!" + "\n" + text
                email = donor.email

                send_mail(
                    "Solicitação de Adoção!", #Título do email
                    message, #Mensagem do email 
                    'settings.EMAIL_HOST_USER', #Host
                    [email], #Destinatário
                    fail_silently=False
                )
 
                return redirect('/home/')
            else:
                return redirect('/login/')
            
class adicionarPet(View):
    @method_decorator(login_required)
    def get(self, request):
        form = RegisterPetForm()
        imgForm_factory = inlineformset_factory(Pet, ImagePet, form=RegisterImgPet, extra=1, max_num=4, min_num=0, validate_min=True) 
        imgForm = imgForm_factory()

        if getUserType(request.user) == 'defaultUser':
            info = getDefaultUser(request.user)
        else:
            info = getCompany(request.user)

        context = {
            'info' : info,
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

        if form.is_valid() and imgForm.is_valid():
            if request.POST.get('identificador') == "adocao":
                pet = form.save(commit=False)
                pet.fk_user = request.user
                pet.save()

                imgForm.instance = pet
                imgForm.save()

                log_entry = LogEntry.objects.create(fk_donor=request.user, breed=pet.breed, sex=pet.sex)
            else:
                pet = form.save(commit=False)
                pet.fk_user = request.user
                pet.save()

                imgForm.instance = pet
                imgForm.save()

                log_entry = LogEntry.objects.create(fk_donor=request.user, breed=pet.breed, sex=pet.sex)
                lostPets = LostPets.objects.create(fk_pet=pet)


            return redirect('/')
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
            'btn': "Salvar",
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
            return redirect('/perfil/')

class meuPerfil(View):
    @method_decorator(login_required)
    @method_decorator(defaultUserRequired)
    def get(self, request,):
        address = Address.objects.get(fk_user=request.user)
        defaultUser = DefaultUser.objects.get(fk_user=request.user)
        profileImage = ProfileImage.objects.get(fk_user=request.user)

        defaultUserForm = DefaultUserForm(instance=defaultUser)
        addressForm = AddressForm(instance=address)
        profileImageForm = ProfileImageForm(instance=profileImage)

        search = request.GET.get('Search') if request.GET.get('Search') != None else ''
    
        pets = []
        pets_fav = []


        user = getDefaultUser(request.user)
        for pet in getMyPets(request.user, search):
            imgs = ImagePet.objects.filter(fk_pet = pet)
            if getTestLostPets(pet) == False:
                pets.append(
                    {
                        'pet' : pet,
                        'imgs': imgs,
                        'type':'myPets'}
                    )
            else:
                pets.append(
                    {
                        'pet' : pet,
                        'imgs': imgs,
                        'type':'myLostPets'}
                    )
            
        for favorite in getFavoritePets(request.user, search):
            pet = favorite.fk_pet
            imgs = ImagePet.objects.filter(fk_pet = favorite.fk_pet)
            contacts = getUserContacts(request, pet)
            favoritePet = getTestFavoritePets(pet)
            pets_fav.append(
                {
                    'pet' : pet,
                    'imgs': imgs,
                    'contacts':contacts,
                    'type': "adot",
                    'favoritePet':favoritePet}
                )
        
        pag = paginator(request, pets)  
        pag_fav = paginator(request, pets_fav)   

        context = {
            'info':user,
            'pets' : pag['pet_page'],
            'pets_fav' :pag_fav['pet_page'],
            'page' : pag['page'],
            'nextPage' : pag['nextPage'], 
            'prevPage' : pag['prevPage'],
            'pages': pag['pages'],
            'petName' : search,
            'addressForm':addressForm,
            'defaultUserForm':defaultUserForm,
            'profileImageForm':profileImageForm
        }
        
        return render(request, 'perfil/perfil.html', context)
    def post(self, request):
        address = Address.objects.get(fk_user=request.user)
        defaultUser = DefaultUser.objects.get(fk_user=request.user)
        profileImage = ProfileImage.objects.get(fk_user=request.user)

        profileImageForm = ProfileImageForm(request.POST, request.FILES, instance=profileImage)
        defaultUserForm = DefaultUserForm(request.POST, instance=defaultUser)
        addressForm = AddressForm(request.POST, instance=address)

        forms = [profileImageForm, defaultUserForm, addressForm]
        if request.POST.get('editName') != None:
            request.user.username = request.POST.get('name')
            request.user.save()
            return redirect('/perfil/')
        if all(form.is_valid() for form in forms):
            for item in forms:
                if item.has_changed():
                    item.save()
        
        return redirect('/perfil/')
        


class petsPerdidos(View):
    def get(self, request):
        search = request.GET.get('Search') if request.GET.get('Search') != None else ''
    
        pets = []

        
        for lostPet in getLostPets(request, search):
            pet = lostPet.fk_pet
            imgs = ImagePet.objects.filter(fk_pet = pet)
            contacts = getUserContacts(request, pet)
            pets.append(
                {
                    'pet' : pet,
                    'imgs': imgs,
                    'contacts':contacts,
                    'type': "lost"}
            )
        pag = paginator(request, pets)
            
        if request.user.is_authenticated:
            context = {
                'info' : getDefaultUser(request.user),
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

            message = donee.username + " enviou uma solitação para a adoção do seu pet " + pet.name + "!"
            email = donor.email

            send_mail(
                "Solicitação de Adoção!", #Título do email
                message, #Mensagem do email 
                'settings.EMAIL_HOST_USER', #Host
                [email], #Destinatário
                fail_silently=False
            )
 
            return redirect('/home/')
        else:
            return redirect('/login/')
    
class favoritePet(View):
    def get(self, request, petId):
        pet = Pet.objects.get(id=petId)
        donee = request.user
        mensage = "O usuário " + donee.username + " está interessado no seu Pet " + pet.name
        testePet = Favorites.objects.filter(fk_pet=pet, fk_donee=donee)
        
        if len(testePet) == 0:
            Notification.objects.create(fk_pet=pet, fk_donee=donee, fk_donor=pet.fk_user, mensage=mensage)
            Favorites.objects.create(fk_pet=pet, fk_donee=donee)
        else:
            testePet[0].delete()
        return redirect('/home/')
    

class MarcarAdotado(View):
    def get(self, request, petId):
        pet = Pet.objects.get(id=petId)

        try:
            pet = LostPets.objects.get(fk_pet = pet)
            pet.found = True
        except:
            pass

        pet.adopted = True
        pet.save()


        #Deletando solicitações pelo pet, pois já foi adotado
        solicitacoes = Requests.objects.filter(fk_pet=pet)
        for solicitacao in solicitacoes:
            solicitacao.delete()

        return redirect('/processos/')
    
def processos(request):
    pets = Pet.objects.filter(fk_user=request.user)
    petsFormatados = []
    petsEmAdocao = []
    petsSolicitados = []
    petsAdotados = []

    for pet in pets:


        #Pegar pets solicitados!
        solicitado = Requests.objects.filter(fk_pet=pet)
        if solicitado.count() > 0:
            requests = Requests.objects.filter(fk_pet=pet)
            imgs = ImagePet.objects.filter(fk_pet=pet)
            contacts = getUserContacts(request, pet)
            petsSolicitados.append(
                {
                    'pet':pet,
                    'imgs': imgs,
                    'contacts':contacts,
                    'type': "requested",
                    'requests': requests,
                }
            )
        
        #Pegar pets que ainda não foram adotados
        elif pet.adopted == False:
            imgs = ImagePet.objects.filter(fk_pet=pet)
            contacts = getUserContacts(request, pet)
            petsEmAdocao.append(
                {
                    'pet':pet,
                    'imgs': imgs,
                    'contacts':contacts,
                    'type': "myPets",
                    'requests': False,
                }
            )


        #Pegar pets já adotados
        if pet.adopted == True:
            imgs = ImagePet.objects.filter(fk_pet=pet)
            contacts = getUserContacts(request, pet)
            petsAdotados.append(
                {
                    'pet':pet,
                    'imgs': imgs,
                    'contacts':contacts,
                    'type': "adopted",
                    'requests': False,
                }
            )
        


    if len(petsEmAdocao) == 0:
        petsEmAdocao = "Empty"
    if len(petsSolicitados) == 0:
        petsSolicitados = "Empty"
    if len(petsAdotados) == 0:
        petsAdotados = "Empty"

    context = {'info':getDefaultUser(request.user), 'petsEmAdocao':petsEmAdocao, 'petsSolicitados':petsSolicitados, 'petsAdotados':petsAdotados}

    return render(request, 'processos/processos.html', context)

