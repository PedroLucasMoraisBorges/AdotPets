from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login, name='login'),
    path('cadastro/', views.Cadastro, name='cadastroUser'),
    path('logout/', views.Logout.as_view(), name='logout')
]