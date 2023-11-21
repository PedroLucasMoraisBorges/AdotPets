from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Pet(models.Model):
    fk_user = models.ForeignKey(User, related_name= 'pet', on_delete= models.CASCADE)
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=30)
    age = models.CharField(max_length=8)
    desc = models.CharField(max_length=200)
    obs = models.CharField(max_length=200)
    sex = models.CharField(max_length=10)
    adopted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class ImagePet(models.Model):
    fk_pet = models.ForeignKey(Pet, related_name = 'imagem_pet', on_delete = models.CASCADE)
    img = models.ImageField(upload_to='imgPet/', blank=False, default='')

class LostPets(models.Model):
    fk_pet = models.ForeignKey(Pet, related_name= 'lostPets', on_delete=models.CASCADE)
    found = models.BooleanField(default=False)

class Requests(models.Model):
    fk_pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    fk_donor = models.ForeignKey(User, related_name='requests_donor', on_delete= models.CASCADE)
    fk_donee = models.ForeignKey(User, related_name='requests_donee', on_delete= models.CASCADE)
    requestText = models.TextField(default="Solicitação de adoção!")
    dt_request = models.DateField(auto_now=True)
    state_choices = [
        ('REQUESTED', 'requested'),
        ('DENIED', 'denied'),
        ('ACCEPTED', 'accepted')
    ]    
    state = models.CharField(max_length=20, choices=state_choices, default="REQUESTED")


class Favorites(models.Model):
    fk_pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    fk_donee = models.ForeignKey(User, on_delete= models.CASCADE)
