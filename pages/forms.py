from . import models
from django import forms
from .models import *



choices = [('M', 'Masculino'), ('F', 'Feminino')]
choicesBreed = [
    ('Pug', 'Pug'),
    ('Shih Tzu', 'Shih Tzu'),
    ('Buldogue', 'Buldogue'),
    ('Pastor Alemão', 'Pastor Alemão'),
    ('Poodle', 'Poodle'),
    ('Rottweiler', 'Rottweiler'),
    ('Labrador', 'Labrador'),
    ('Pinscher', 'Pinscher'),
    ('Golden Retriever', 'Golden Retriever'),
    ('Caramelo', 'Caramelo')]

choicesSex = [
    ('Macho', 'Macho'),
    ('Fêmea', 'Fêmea')
]

class RegisterPetForm(forms.ModelForm):
    name = forms.CharField(label='Nome do seu Pet:', widget=forms.TextInput(attrs={'class':'input-pet-information', 'placeholder':'Digite o nome do pet aqui'}))
    breed = forms.ChoiceField(label='Raça', choices=[('', 'Selecione a Raça')]+choicesBreed, widget=forms.Select(attrs={'class':'input-pet-information'}))
    desc = forms.CharField(label='Descrição do animal:', widget=forms.TextInput(attrs={'class':'input-pet-information', 'placeholder': 'Digite a descrição do pet aqui'}))
    age = forms.IntegerField(label='Idade', widget=forms.NumberInput(attrs={'class':'input-pet-information input-idade', 'placeholder':'Idade em anos'}))
    obs = forms.CharField(label='Observações', widget=forms.TextInput(attrs={'class':'input-pet-information', 'placeholder':'Digite as observações aqui'}))
    sex = forms.ChoiceField(label='Sexo', choices=choicesSex, widget=forms.RadioSelect(attrs={'class':'radio-inputs'}))

    class Meta:
        model = Pet
        fields = ['name', 'desc', 'obs', 'age', 'sex','breed',]

class RegisterImgPet(forms.ModelForm):
    img = forms.ImageField(required=True, label=None)
    class Meta:
        model = ImagePet
        fields = ['img',]