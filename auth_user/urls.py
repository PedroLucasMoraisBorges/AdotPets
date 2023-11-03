from django.urls import path
from . import views

urlpatterns = [
    # Acesso
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

    #Cadastro
    path('cadastro/cliente/', views.registerCliente.as_view(), name='cadastroCliente'),
    path('cadastro/company/', views.registerCompany.as_view(), name='cadastrocompany')

    #Edição
]