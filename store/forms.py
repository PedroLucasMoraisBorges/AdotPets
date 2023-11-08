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
        widget= forms.TextInput(attrs={'class': 'input-pet-information'}),
        required=True,
        label='Nome do produto'
    )
    
    desc = forms.CharField(
        widget= forms.TextInput(attrs={'class': 'input-pet-information'}),
        required=True,
        label= 'Descrição'
    )
    
    value = forms.IntegerField(
        widget= forms.NumberInput(attrs={'class': 'input-pet-information', 'min':0}),
        label= 'Valor'
    )
    
    category = forms.ChoiceField(
        widget= forms.Select(attrs={'class' : 'category input-pet-information'}),
        required= True,
        choices=[('', 'Selecione a Categoria')]+categoryChoices
    )
    discount = forms.FloatField(
        label= 'Desconto',
        widget= forms.NumberInput(attrs={'class':'input-pet-information'}),
        required=False
    )
    divided = forms.IntegerField(
        label='Dividir sem juros',
        widget= forms.NumberInput(attrs={'class':'input-pet-information'}),
        required=True
    )

    class Meta:
        model = Product
        fields = ['name', 'desc', 'value', 'category', 'discount', 'divided',]


class ProductImgForm(forms.ModelForm):
    img = forms.ImageField(required=True, label=None)
    class Meta:
        model = ProductImage
        fields = ['img',]
