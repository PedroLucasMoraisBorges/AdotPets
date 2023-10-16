from django.shortcuts import render, redirect, HttpResponse
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
    return render(request, 'homeOficial.html')

class homePage(View):
    @method_decorator(login_required)
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
            
            defaultUser = DefaultUser.objects.get(fk_user = request.user)
            context = {
                'defaultUser' : defaultUser,
                'pets' : pets
            }
            return render(request, 'adocao/home.html', context)
        else:
            print("vv")


            
class adicionarPet(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CadastrarPetForm()
        CadastrarPetFormset = inlineformset_factory(Pet, ImagemPet, form=CadastroImagemForm, extra=1, max_num=4, min_num=0, validate_min=True) 
        imgForm = CadastrarPetFormset()

        context = {
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
                {
                    'pet' : pet,
                    'imgs': imgs}
                )

        context = {
            'pets' : pets
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
            'pets' : pets
        }
        return render(request, 'perdidos/petsPerdidos.html', context)
    
def cadastroProduto(request):
    if request.POST:
        teste = uploadProduto(request.POST)
        if teste.is_valid():
            teste.save()
            print("É válido e foi salvo.")
        return redirect(produtos)
    return render(request, 'cadastros/cadastroProduto.html', {'form' : teste})

def produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'produtos/produtos.html', {'produto': produtos})

def verProduto(request, id):
    var = Produto.objects.filter(id=id)
    if var != None:
        return render(request, 'produtos/produto.html', {'produto' : var})
    else:
        return HttpResponse("Esse produto não existe! Var = %s" %var)

def verLoja(request, id):
    id_emp = Empresa.objects.get(pk=id)
    produtos = Produto.objects.filter(empresa=id_emp)
    return render(request, 'produtos/loja.html', {'produto' : produtos, 'empresa' : id_emp})

def cadastroProduto(request):
    if request.method == 'POST':
        teste = uploadProduto(request.POST)

        if teste.is_valid():
            teste.save()
            print("É válido e foi salvo.")
        return redirect(produtos)

    return render(request, 'cadastroProduto.html', {'form' : uploadProduto})

def editarProduto(request, id):
    var = Produto.objects.get(id=id)
    form = editProduto(request.POST or None, instance=var)
    if form.is_valid():
        form.save()
        print("É válido e foi salvo.")
        return redirect(produtos)

    return render(request, 'editarProduto.html', {'produto' : var, 'form' : form})