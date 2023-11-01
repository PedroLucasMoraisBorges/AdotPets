from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import NumberInput, FileInput
from .models import *


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='E-mail',
        widget = forms.TextInput(attrs={'class': 'px-3 py-2 w-100 border-radius-inputs border fs-inputs shadow-sm', 'placeholder': 'Email'}))
    
    nome = forms.CharField(
        required=True,
        label='Nome completo',
        widget = forms.TextInput(attrs={'class': 'none px-3 py-2 w-100 border-radius-inputs border fs-inputs shadow-sm', 'placeholder': 'Nome completo'}))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'minlength':'8'}))

    class Meta:
        model = User
        fields = ['nome', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.nome = self.cleaned_data['nome']
        if commit:
            user.save()
        return user

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if not nome:
            raise forms.ValidationError('Por favor, informe seu nome completo.')
        return nome

class DefaultUserForm(forms.ModelForm):
    telephone = forms.CharField(
        label = 'telephone',
        widget = forms.NumberInput(attrs={'class': 'none px-3 py-2 w-100 border-radius-inputs border fs-inputs shadow-sm', 'placeholder': '88999999999'}))
    
    class Meta:
        model = DefaultUser
        fields = '__all__'
        exclude = ('fk_user',)

class ProfileImageForm(forms.ModelForm):
    img = forms.ImageField(
        label='Imagem de perfil',
        widget= FileInput(attrs={'accept':'.jpg, .png','class':'none'}),
        help_text='Tipos de documentos aceitos: .jpg, .png',
        required=False
    )

    class Meta:
        model = ProfileImage
        fields = '__all__'
        exclude = ('fk_user',)

class AddressForm(forms.ModelForm):
    cep = forms.IntegerField(
        label = 'Cep',
        widget = forms.NumberInput(attrs={'class': 'none px-3 py-2 w-100 border-radius-inputs border fs-inputs shadow-sm', 'placeholder': '00000000'})
    )
    city = forms.CharField(
        label= 'city',
        widget = forms.TextInput(attrs={'class': 'none px-3 py-2 w-100 border-radius-inputs border fs-inputs shadow-sm', 'placeholder': 'city'})
    )
    road = forms.CharField(
        label= 'Rua',
        widget = forms.TextInput(attrs={'class': 'none px-3 py-2 w-100 border-radius-inputs border fs-inputs shadow-sm', 'placeholder': 'Informe a sua rua'})
    )
    number = forms.IntegerField(
        label='Número',
        widget = forms.NumberInput(attrs={'class': 'none px-3 py-2 w-100 border-radius-inputs border fs-inputs shadow-sm', 'placeholder': '1000'})
    )

    class Meta:
        model = Address
        fields = '__all__'
        exclude = ('fk_user',)

class CompanyForm(forms.ModelForm):
    social_name = forms.CharField(
        label='Nome Social',
        widget = forms.TextInput(attrs={'class': 'px-3 py-2 w-100 border-radius-inputs border fs-inputs shadow-sm', 'placeholder': 'Nome Social'})
    )
    fantasy_name = forms.CharField(
        label='Nome Fantasia',
        widget = forms.TextInput(attrs={'class': 'px-3 py-2 w-100 border-radius-inputs border fs-inputs shadow-sm', 'placeholder': 'Nome Fantasia'})
    )
    cnpj = forms.IntegerField(
        label='Cnpj',
        widget = forms.NumberInput(attrs={'class': 'px-3 py-2 w-100 border-radius-inputs border fs-inputs shadow-sm', 'placeholder': '0000000000000'})
    )
    class Meta:
        model = Company
        fields = '__all__'
        exclude = ('fk_user',)