from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Pet(models.Model):
    fk_user = models.ForeignKey(User, related_name= 'pet', on_delete= models.CASCADE)
    nome = models.CharField(max_length=50)
    raca = models.CharField(max_length=30)
    idade = models.CharField(max_length=8)
    desc = models.CharField(max_length=200)
    obs = models.CharField(max_length=200)
    sexo = models.CharField(max_length=10)

    def __str__(self):
        return self.nome
    

class ImagemPet(models.Model):
    fk_pet = models.ForeignKey(Pet, related_name = 'imagem_pet', on_delete = models.CASCADE)
    imagem = models.ImageField(upload_to='imgPet/', blank=False, default='')

class AnimaisPerdidos(models.Model):
    fk_pet = models.ForeignKey(Pet, related_name= 'animaisPerdidos', on_delete=models.CASCADE)

class AnimaisEncontrados(models.Model):
    fk_pet = models.ForeignKey(Pet, related_name= 'animaisEncontrados', on_delete=models.CASCADE)

class Requisicoes(models.Model):
    fk_pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    fk_doador = models.ForeignKey(User, related_name='requisicoes_doador', on_delete= models.CASCADE)
    fk_donatario = models.ForeignKey(User, related_name='requisicoes_donatario', on_delete= models.CASCADE)

class Favoritos(models.Model):
    fk_pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    fk_donatario = models.ForeignKey(User, on_delete= models.CASCADE)