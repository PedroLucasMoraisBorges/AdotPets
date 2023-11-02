from django.shortcuts import render, redirect, HttpResponse
from auth_user import *
from .models import *
from .forms import *
from pages.decorator import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from pages.utilits import *
from django.views import View


def produtos(request):
    produtos = Product.objects.all()

    context = {
        'produtos' : produtos,
        'info' : getDefaultUser(request.user)
    }
    return render(request, 'loja/produtos.html', context)


def verProduto(request, id):
    var = Product.objects.filter(id=id)
    if var != None:
        return render(request, 'produtos/produto.html', {'produto' : var})
    else:
        return HttpResponse("Esse produto não existe! Var = %s" %var)

def verLoja(request, id):
    company = Company.objects.get(pk=id)
    products = Product.objects.filter(empresa=company)
    return render(request, 'produtos/loja.html', {'produto' : products, 'empresa' : company})

class HomeCompany(View):
    @method_decorator(login_required)
    @method_decorator(companyRequired)
    def get(self, request):
        search = request.GET.get('Search') if request.GET.get('Search') != None else ''
        info = getCompany(request.user)
        pets = []

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
            
        context = {
            'info' : info,
            'products' : getCompanyProducts(info['company']),
            'pets' : pets
        }

        return render(request, 'company/homeCompany.html', context)


class InsertProduct(View):
    @method_decorator(companyRequired)
    @method_decorator(login_required)
    def get(self, request):
        productFrom = ProductForm()
    def post(self, request):
        productForm = ProductForm(request.POST)

        if productForm.is_valid():
            productForm.save()
            print("É válido e foi salvo.")
        return redirect(produtos)


def editarProduto(request, id):
    product = Product.objects.get(id=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        print("É válido e foi salvo.")
        return redirect(produtos)

    return render(request, 'editarProduto.html', {'produto' : product, 'form' : form})