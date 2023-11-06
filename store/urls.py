from django.urls import path
from . import views

urlpatterns = [
    path("Empresa/", views.HomeCompany.as_view(), name='homeCompany'),
    path("cadastros/cadastroProduto", views.InsertProduct.as_view(), name="cadastroProduto"),
    path("produtos/editarProduto/<int:id>", views.editarProduto, name="editarProduto"),
    path("produtos/", views.Loja.as_view(), name="produtos"),
    path("produtos/produto/<int:id>", views.verProduto, name="verProduto"),
    path("produtos/loja/<int:id>", views.verLoja, name="verLoja")
]