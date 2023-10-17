from django.db import models
from .managers import*
from django.contrib.auth.models import User
from pages.models import *

# Create your models here.
class DefaultUser(models.Model):
    fk_user = models.ForeignKey(User, related_name = 'defaultUser', on_delete = models.CASCADE)
    telefone = models.CharField(unique= True, blank= False, max_length= 14)

class Empresa(models.Model):
    fk_user = models.ForeignKey(User, related_name= 'empresa', on_delete= models.CASCADE)
    nome_social = models.CharField(unique= True, blank=False, max_length=75)
    nome_fantasia = models.CharField(unique= True, blank=False, max_length=75)
    cnpj = models.CharField(unique=True, max_length=18)

class Endereco(models.Model):
    fk_user = models.ForeignKey(User, related_name= 'endereco', on_delete= models.CASCADE)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=75)
    rua = models.CharField(max_length=80)
    numero = models.IntegerField()

class Servicos(models.Model):
    fk_empresa = models.ForeignKey(Empresa, related_name='servicos', on_delete= models.CASCADE)
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=150)

# Tabela para logs

class LogEntrada(models.Model):
    fk_doador = models.ForeignKey(User, related_name= 'doador_entrada', on_delete= models.CASCADE)
    raca = models.CharField(max_length=75)
    sexo = models.CharField(max_length=15)
    dt_entrada = models.DateTimeField()

class LogSaida(models.Model):
    fk_doador = models.ForeignKey(User, related_name= 'doador_saida', on_delete= models.CASCADE)
    fk_donatario = models.ForeignKey(User, related_name= 'donatario', on_delete= models.CASCADE)
    fk_pet = models.ForeignKey(Pet, related_name= 'pet', on_delete= models.CASCADE)
    dt_saida = models.DateTimeField()
    qt_saida = models.IntegerField()

#Tabela de pontos 

class Pontos(models.Model):
    user = models.ForeignKey(User, related_name='pontos' ,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    spent = models.IntegerField()
    updated = models.DateTimeField(auto_now=True)

