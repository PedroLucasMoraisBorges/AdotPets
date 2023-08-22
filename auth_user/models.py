from django.db import models
from .managres import*

# Create your models here.
class User(models.Model):
    username = None
    email = models.EmailField(unique = True, blank = False)
    nome = models.CharField(max_length = 50)
    telefone = models.CharField(max_length = 13)
    telefone_fixo = models.CharField(max_length = 12, blank = True, null = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    object = UserManager()

    def __str__(self):
        return self.nome