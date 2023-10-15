from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingPage, name='landingPage'),
    path('home/', views.homePage.as_view(), name='home'),
    path('cadastroPet/', views.adicionarPet.as_view(), name='uploadPet'),
    path('editarPet/<int:id>', views.editarPet.as_view(), name='editarPet'),
    path('meus_Pets/', views.meusPets.as_view(), name='meusPets'),
    path('petsPerdidos/', views.petsPerdidos.as_view(), name='petsPerdidos'),
    path("cadastroProduto", views.cadastroProduto, name="cadastroProduto"),
    path("produtos/", views.produtos, name="produtos"),
    path("produto/<int:id>", views.verProduto, name="verProduto"),
    path("loja/<int:id>", views.verLoja, name="verLoja")
]