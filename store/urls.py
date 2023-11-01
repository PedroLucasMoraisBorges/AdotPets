from django.contrib import admin
from django.urls import path
from . import views

url_parents = [
    path("cadastros/cadastroProduto", views.cadastroProduto, name="cadastroProduto"),
    path("produtos/editarProduto/<int:id>", views.editarProduto, name="editarProduto"),
    path("produtos/produtos/", views.produtos, name="produtos"),
    path("produtos/produto/<int:id>", views.verProduto, name="verProduto"),
    path("produtos/loja/<int:id>", views.verLoja, name="verLoja")
]