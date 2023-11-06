from django.shortcuts import render, redirect, HttpResponse
from auth_user import *
from .models import *
from .forms import *

from pages.decorator import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from pages.utilits import *
from django.views import View


class Loja(View):
    def get(self, request):
        search = request.GET.get('Search') if request.GET.get('Search') != None else ''

        products = getAllProcuts(search)

        productsList = []
        for product in products:
            img = ProductImage.objects.get(fk_product = product)
            print(img.img.url)
            productsList.append({
                'product' : product,
                'productImg' : img
            })

        context = {
            'productsList' : productsList,
            'info' : getDefaultUser(request.user),
            'search' : search
        }

        return render(request, 'loja/produtos.html', context)
    


def verProduto(request, id):
    var = Product.objects.filter(id=id)
    if var != None:
        return render(request, 'produtos/produto.html', {'produto' : var})
    else:
        return HttpResponse("Esse produto não existe! Var = %s" %var)

def verLoja(request, id):
    company = Company.objects.get(fk_user=request.user)
    products = Product.objects.filter(fk_company=company)
    
    productsList = []
    for product in products:
        img = ProductImage.objects.get(fk_product = product)
        print(img.img.url)
        productsList.append({
            'product' : product,
            'productImg' : img
        })
    
    context = {
        'info' : getCompany(request.user),
        'productsList' : productsList,
        'company' : company
    }
    return render(request, 'loja/loja.html', context)


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


    