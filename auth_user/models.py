from django.db import models
from .managers import*
from django.contrib.auth.models import User

# Create your models here.
class DefaultUser(models.Model):
    fk_user = models.ForeignKey(User, related_name = 'defaultUser', on_delete = models.CASCADE)
    telefone = models.CharField(unique= True, blank= False, max_length= 13)