from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingPage.as_view(), name='landingPage'),
    path('home/', views.homePage.as_view(), name='home'),
    path('cadastroPet/', views.adicionarPet.as_view(), name='uploadPet'),
    path('editarPet/<int:id>', views.editarPet.as_view(), name='editarPet'),
    path('meus_Pets/', views.meuPerfil.as_view(), name='meusPets'),
    path('petsPerdidos/', views.petsPerdidos.as_view(), name='petsPerdidos'),
    path('adotarPet/<int:petId>/<int:doadorId>', views.adotarPet.as_view(), name='adotarPet'),
    path('favoritarPet/<int:petId>', views.favoritarPet.as_view(), name='favoritarPet'),
]