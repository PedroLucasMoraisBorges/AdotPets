from django.urls import path
from . import views

urlpatterns = [
    # Acesso
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

    #Cadastro
    path('cadastro/cliente/', views.cadastroCliente.as_view(), name='cadastroCliente'),
    path('cadastro/empresa/', views.cadastroEmpresa.as_view(), name='cadastroEmpresa')

    #Edição
]