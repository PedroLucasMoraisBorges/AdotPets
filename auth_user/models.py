from django.db import models
from .managers import*
from django.contrib.auth.models import User
from pages.models import *

# Create your models here.
class DefaultUser(models.Model):
    fk_user = models.ForeignKey(User, related_name = 'defaultUser', on_delete = models.CASCADE)
    telephone = models.CharField(unique= True, blank= False, max_length= 14)

class ProfileImage(models.Model):
    fk_user = models.ForeignKey(User, related_name = 'profileImage', on_delete = models.CASCADE)
    img = models.ImageField(upload_to='profile_image/', blank=True, null=True)

class Company(models.Model):
    fk_user = models.ForeignKey(User, related_name= 'company', on_delete= models.CASCADE)
    social_name = models.CharField(unique= True, blank=False, max_length=75)
    fantasy_name = models.CharField(unique= True, blank=False, max_length=75)
    cnpj = models.CharField(unique=True, max_length=18)
    telephone = models.CharField(unique= True, blank= False, max_length= 14, default='')

class Address(models.Model):
    fk_user = models.ForeignKey(User, related_name= 'address', on_delete= models.CASCADE)
    cep = models.CharField(max_length=8)
    city = models.CharField(max_length=75)
    road = models.CharField(max_length=80)
    number = models.IntegerField()

class Servicos(models.Model):
    fk_company = models.ForeignKey(Company, related_name='servicos', on_delete= models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)

# Tabela para logs

class LogEntry(models.Model):
    fk_donor = models.ForeignKey(User, related_name= 'doador_entrada', on_delete= models.CASCADE)
    breed = models.CharField(max_length=75)
    sex = models.CharField(max_length=15)
    dt_entry = models.DateTimeField(auto_now=True)

class LogExit(models.Model):
    fk_donor = models.ForeignKey(User, related_name= 'donor', on_delete= models.CASCADE)
    fk_donee = models.ForeignKey(User, related_name= 'donee', on_delete= models.CASCADE)
    fk_pet = models.ForeignKey(Pet, related_name= 'pet', on_delete= models.CASCADE)
    dt_exit = models.DateTimeField(auto_now=True)

#Tabela de pontos 

class Pontos(models.Model):
    user = models.ForeignKey(User, related_name='pontos' ,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    spent = models.IntegerField()
    updated = models.DateTimeField(auto_now=True)

class Notification(models.Model):
    fk_donor = models.ForeignKey(User, related_name='NotificationDonor', on_delete=models.CASCADE)
    fk_donee = models.ForeignKey(User, related_name='NotificationDonee', on_delete=models.CASCADE)
    fk_pet = models.ForeignKey(Pet, related_name='NotificationPet', on_delete=models.CASCADE)
    mensage = models.CharField(max_length=255)
