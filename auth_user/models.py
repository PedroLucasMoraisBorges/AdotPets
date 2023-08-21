from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(unique = True, blank = False)
    nome = models.CharField(max_length = 50)
    telefone = models.CharField(max_length = 13)
    telefone_fixo = models.CharField(max_length = 12, blank = True, null = True)