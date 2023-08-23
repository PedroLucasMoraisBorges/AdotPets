from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import NumberInput
from .models import *


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='E-mail',
        widget = forms.TextInput(attrs={'class': 'px-3 py-2 w-100 border-radius-inputs border fs-inputs shadow-sm', 'placeholder': 'Email'}))
    
    nome = forms.CharField(
        required=True,
        label='Nome completo',
        widget = forms.TextInput(attrs={'class': 'px-3 py-2 w-100 border-radius-inputs border fs-inputs shadow-sm', 'placeholder': 'Email'}))

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
    telefone = forms.CharField(
        label = 'Telefone',
        widget = forms.NumberInput(attrs={'class': 'px-3 py-2 w-100 border-radius-inputs border fs-inputs shadow-sm', 'placeholder': 'Telefone'}))
    
    class Meta:
        model = defaultUser
        fields = '__all__'
        exclude = ('fk_user',)