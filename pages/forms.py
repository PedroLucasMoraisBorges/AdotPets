from . import models
from django import forms
from .models import *



choices = [('M', 'Masculino'), ('F', 'Feminino')]
choicesRacas = [
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

class CadastrarPetForm(forms.ModelForm):
    nome = forms.CharField(label='Nome')
    idade = forms.IntegerField(label='Idade')
    raca = forms.ChoiceField(label='Raça', choices=[('', 'Selecione a Raça')]+choicesRacas)
    desc = forms.CharField(label='Descrição')
    obs = forms.CharField(label='Observações')
    sexo = forms.ChoiceField(label='Sexo', choices=[('', 'Selecione o sexo...')] + choices)

    class Meta:
        model = Pet
        fields = ['nome', 'idade', 'desc', 'obs', 'sexo','raca',]

class CadastroImagemForm(forms.ModelForm):
    imagem = forms.ImageField()
    class Meta:
        model = ImagemPet
        fields = ['imagem',]
