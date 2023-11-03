from . import models
from django import forms
from .models import *
from auth_user.models import Company

categoryChoices = [
    ('Medicamento', 'Medicamento'),
    ('Cuidados', 'Cuidados'),
    ('Alimentação', 'Alimentação')
]

class ProductForm(forms.ModelForm):
    name = forms.CharField(
        widget= forms.TextInput(attrs={'required': True}),
        label='Nome do produto')
    desc = forms.CharField(
        widget= forms.TextInput(attrs={'required': True}),
        label= 'Descrição')
    value = forms.IntegerField(
        widget= forms.NumberInput(attrs={'required': True, 'min':0}),
        label= 'Valor')
    category = forms.ChoiceField(
        widget= forms.Select(attrs={'class' : 'category'}),
        required= True,
        choices=[('', 'Selecione a Categoria')]+categoryChoices
    )
    discount = forms.FloatField(
        label= 'Desconto',
        required=False
    )

    class Meta:
        model = Product
        fields = ['name', 'desc', 'value', 'category']


class ProductImgForm(forms.ModelForm):
    img = forms.ImageField(required=True, label=None)
    class Meta:
        model = ProductImage
        fields = ['img',]
