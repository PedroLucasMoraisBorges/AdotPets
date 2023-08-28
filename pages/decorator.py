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