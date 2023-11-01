from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #LandingPage
    path('', views.landingPage.as_view(), name='landingPage'),
    
    #Amostra de pets
    path('petsPerdidos/', views.petsPerdidos.as_view(), name='petsPerdidos'),

    path("cadastros/cadastroProduto", views.cadastroProduto, name="cadastroProduto"),
    path("produtos/editarProduto/<int:id>", views.editarProduto, name="editarProduto"),
    path("produtos/produtos/", views.produtos, name="produtos"),
    path("produtos/produto/<int:id>", views.verProduto, name="verProduto"),
    path("produtos/loja/<int:id>", views.verLoja, name="verLoja")

    path('home/', views.homePage.as_view(), name='home'),

    #perfil
    path('perfil/', views.meuPerfil.as_view(), name='perfil'),
    
    #Interação com Pet
    path('cadastroPet/', views.adicionarPet.as_view(), name='cadastroPet'),
    path('editarPet/<int:id>', views.editPet.as_view(), name='editarPet'),
    path('adotarPet/<int:petId>/<int:doadorId>', views.adotarPet.as_view(), name='adotarPet'),
    path('favoritarPet/<int:petId>', views.favoritePet.as_view(), name='favoritarPet'),
    path('marcarAdotado/<int:petId>', views.MarcarAdotado.as_view(), name='marcarAdotado')
]