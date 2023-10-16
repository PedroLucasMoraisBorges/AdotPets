from .models import *
from auth_user import models
from django.db.models import Q

def getPetsAdot(user, search):
    pets = reversed(Pet.objects.filter(~Q(fk_user=user)).filter(Q(nome__istartswith=search) and Q(raca__istartswith=search) and Q(sexo__istartswith=search)))
    return pets

def getMyPets(user, search):
    pets = reversed(Pet.objects.filter(Q(fk_user=user)).filter(Q(nome__istartswith=search) and Q(raca__istartswith=search) and Q(sexo__istartswith=search)))
    return pets

def getLostPets(user, search):
    pets = reversed(AnimaisPerdidos.objects.filter(~Q(fk_pet__fk_user=user)).filter(Q(fk_pet__nome__istartswith=search) and Q(fk_pet__raca__istartswith=search) and Q(fk_pet__sexo__istartswith=search)))
    return pets

    