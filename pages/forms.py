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

choicesSexo = [
    ('Macho', 'Macho'),
    ('Fêmea', 'Fêmea')
]

class CadastrarPetForm(forms.ModelForm):
    nome = forms.CharField(label='Nome do seu Pet:', widget=forms.TextInput(attrs={'class':'input-pet-information', 'placeholder':'Digite o nome do pet aqui'}))
    raca = forms.ChoiceField(label='Raça', choices=[('', 'Selecione a Raça')]+choicesRacas, widget=forms.Select(attrs={'class':'input-pet-information'}))
    desc = forms.CharField(label='Descrição do animal:', widget=forms.TextInput(attrs={'class':'input-pet-information', 'placeholder': 'Digite a descrição do pet aqui'}))
    idade = forms.IntegerField(label='Idade', widget=forms.NumberInput(attrs={'class':'input-pet-information input-idade', 'placeholder':'Idade em anos'}))
    obs = forms.CharField(label='Observações', widget=forms.TextInput(attrs={'class':'input-pet-information', 'placeholder':'Digite as observações aqui'}))
    sexo = forms.ChoiceField(label='Sexo', choices=choicesSexo, widget=forms.RadioSelect(attrs={'class':'radio-inputs'}))

    class Meta:
        model = Pet
        fields = ['nome', 'desc', 'obs', 'idade', 'sexo','raca',]

class CadastroImagemForm(forms.ModelForm):
    imagem = forms.ImageField(required=True)
    class Meta:
        model = ImagemPet
        fields = ['imagem',]
