from . import models
from django import forms
from .models import Pet

choices = [('M', 'Masculino'), ('F', 'Feminino')]

class cadastrarPet(forms.ModelForm):
    nome = forms.CharField(label='Nome')
    idade = forms.IntegerField()
    desc = forms.CharField(label='Descrição')
    pref = forms.CharField(label='Preferência')
    sexo = forms.ChoiceField(label='Sexo', choices=[('', 'Selecione o sexo...')] + choices)
    imagem = forms.ImageField()

    class Meta:
        model = Pet
        fields = ['nome', 'idade', 'desc', 'pref', 'sexo', 'imagem']