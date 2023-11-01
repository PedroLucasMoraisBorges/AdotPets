from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .forms import *
from .backends import EmailBackend

class Logout(View):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')
    

def Login(request):
    if request.method == 'GET':
        return render(request, 'login/login.html')
    else:
        if request.POST.get('cad') == None:
            email = request.POST.get('email')
            password = request.POST.get('senha')
            user = authenticate(username=email, password=password)

            if user:
                login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                context = {'backErrorMessage':"<div class='errors-header'>Erro de Login encontrado: </div><li>Informações de login incorretas!</li>"}
                return render(request, 'login/login.html', context)
        else:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password == password2:
                user = User.objects.filter(email=email).first()

                if user:
                    context = {'backErrorMessage':"<div class='errors-header'>Erro de cadastro encontrado: </div><li>E-mail já está cadastrado!</li>"}
                    return render(request, 'login/login.html', context)
                else:
                    user = User.objects.create_user(username=username,email=email,password=password)
                    user.save()
                    
                    user = authenticate(username=email, password=password)
                    login(request, user)

                    if request.POST.get('userType') == 'E':
                        return redirect('/cadastro/company/')
                    else:
                        return redirect('/cadastro/cliente/')

class registerCliente(View):
    def get(self, request):
        clientForm = DefaultUserForm()
        addressForm = AddressForm()
        profileImageForm = ProfileImageForm()

        context = {
            'clienteForm' : clientForm,
            'addressForm' : addressForm,
            'profileImageForm':profileImageForm
        }
        return render(request, 'cadastros/cadastroCliente.html', context)
    def post(self, request):
        clientForm = DefaultUserForm(request.POST)
        addressForm = AddressForm(request.POST)
        profileImageForm = ProfileImageForm(request.POST, request.FILES)
        normalForms = [clientForm, addressForm, profileImageForm]

        if all(form.is_valid() for form in normalForms):
            for item in normalForms:
                form = item.save(commit=False)
                form.fk_user = request.user
                form.save()
            return redirect('/home/')
        else:
            context = {
            'clienteForm' : clientForm,
            'addressForm' : addressForm,
            'profileImageForm':profileImageForm
            }
            return render(request, 'cadastros/cadastroCliente.html', context)


class registerCompany(View):
    def get(self, request):
        companyForm = CompanyForm()
        addressForm = AddressForm()
        profileImageForm = ProfileImageForm()

        context = {
            'companyForm' : companyForm,
            'addressForm' : addressForm,
            'profileImageForm':profileImageForm
        }

        return render(request, 'cadastros/cadastrocompany.html', context)
    def post(self, request):
        companyForm = CompanyForm(request.POST)
        addressForm = AddressForm(request.POST)
        profileImageForm = ProfileImageForm(request.POST, request.FILES)
        normalForms = [companyForm, addressForm, profileImageForm]

        if all(form.is_valid() for form in normalForms):
            for item in normalForms:
                form = item.save(commit=False)
                form.fk_user = request.user
                form.save()
            return redirect('/')
        else:
            context = {
            'companyForm' : companyForm,
            'addressForm' : addressForm,
            'profileImageForm':profileImageForm
            }
            return render(request, 'cadastros/cadastrocompany.html', context)
