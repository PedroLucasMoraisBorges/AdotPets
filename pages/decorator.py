from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from auth_user.models import *

def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def defaultUserRequired(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = DefaultUser.objects.get(fk_user=request.user)
        print(user)
        if user is not None:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')
    return wrapper_func

def empresaRequired(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = Empresa.objects.get(fk_user=request.user)
        if user is not None:
            return view_func(request, *args, **kwargs)
        else: 
            return HttpResponseRedirect('/')
    return wrapper_func