from django.shortcuts import render, redirect, HttpResponse
from auth_user import *
from .models import *
from .forms import *

def produtos(request):
    produtos = Product.objects.all()
    return render(request, 'loja/produtos.html', {'produto': produtos})

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

def cadastroProduto(request):
    if request.method == 'POST':
        productForm = ProductForm(request.POST)

        if productForm.is_valid():
            productForm.save()
            print("É válido e foi salvo.")
        return redirect(produtos)

    return render(request, 'cadastros/cadastroProduto.html', {'form' : productForm})

def editarProduto(request, id):
    product = Product.objects.get(id=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        print("É válido e foi salvo.")
        return redirect(produtos)

    return render(request, 'editarProduto.html', {'produto' : product, 'form' : form})