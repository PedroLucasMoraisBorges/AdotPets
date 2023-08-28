from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import HttpResponseRedirect
from .models import *

def Cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastros/cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('password1')
        senha2 = request.POST.get('password2')
        telefone = request.POST.get('telefone')

        if senha == senha2:
            user = User.objects.filter(email=email).first()

            if user:
                return HttpResponse('user já cadastrado')
            else:
                user = User.objects.create_user(username=email,email=email,password=senha,first_name=username)
                user.save()

                defaultUser = DefaultUser.objects.create(telefone=telefone, fk_user=user)
                defaultUser.save()
                
                user = authenticate(username=email, password=senha)
                login(request, user)
                return HttpResponseRedirect('/home/')
            


def Login(request):
    if request.method == 'GET':
        return render(request, 'login/login.html')
    else:
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = authenticate(username=email, password=senha)

        if user:
            login(request, user)
            return HttpResponseRedirect('/home/')