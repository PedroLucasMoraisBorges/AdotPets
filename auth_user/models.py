from django.db import models
from .managres import*
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique = True, blank = False)
    nome = models.CharField(max_length = 50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    objects = UserManager()

    def __str__(self):
        return self.nome

class Empresa(models.Model):
    nome_fantasia = models.CharField(max_length=50)

class defaultUser(models.Model):
    fk_user = models.ForeignKey(User, related_name = 'defaultUser', on_delete = models.CASCADE)
    telefone = models.CharField(unique= True, blank= False, max_length= 13)