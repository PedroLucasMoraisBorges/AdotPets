from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Pet(models.Model):
    fk_user = models.ForeignKey(User, related_name= 'pet', on_delete= models.CASCADE)
    nome = models.CharField(max_length=50)
    idade = models.CharField(max_length=8)
    desc = models.CharField(max_length=200)
    pref = models.CharField(max_length=200)
    sexo = models.CharField(max_length=10)

class ImagemPet(models.Model):
    fk_pet = models.ForeignKey(Pet, related_name = 'imagem_pet', on_delete = models.CASCADE)
    imagem = models.FileField(upload_to='media/imgPet')
