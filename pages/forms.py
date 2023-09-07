from . import models
from django import forms
from .models import *



choices = [('M', 'Masculino'), ('F', 'Feminino')]

class CadastrarPetForm(forms.ModelForm):
    nome = forms.CharField(label='Nome')
    idade = forms.IntegerField(label='Idade')
    desc = forms.CharField(label='Descrição')
    pref = forms.CharField(label='Preferência')
    sexo = forms.ChoiceField(label='Sexo', choices=[('', 'Selecione o sexo...')] + choices)

    class Meta:
        model = Pet
        fields = ['nome', 'idade', 'desc', 'pref', 'sexo',]

class CadastroImagemForm(forms.ModelForm):
    imagem = forms.ImageField()
    class Meta:
        model = ImagemPet
        fields = ['imagem',]
