from django.urls import path
from . import views

urlpatterns = [
    #LandingPage
    path('', views.landingPage.as_view(), name='landingPage'),
    
    #Amostra de pets
    path('petsPerdidos/', views.petsPerdidos.as_view(), name='petsPerdidos'),
    path('home/', views.homePage.as_view(), name='home'),
    path('processos/', views.processos, name='processos'),

    #perfil
    path('perfil/', views.meuPerfil.as_view(), name='perfil'),
    
    #Interação com Pet
    path('cadastroPet/', views.adicionarPet.as_view(), name='cadastroPet'),
    path('editarPet/<int:id>', views.editPet.as_view(), name='editarPet'),
    path('adotarPet/<int:petId>/<int:doadorId>', views.adotarPet.as_view(), name='adotarPet'),
    path('favoritarPet/<int:petId>', views.favoritePet.as_view(), name='favoritarPet'),
    path('marcarAdotado/<int:petId>', views.MarcarAdotado.as_view(), name='marcarAdotado'),
]
