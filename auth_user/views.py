from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.views import View
from .models import *
from .forms import *

# Create your views here.
class Login(View):

    #@method_decorator(authenticated_user)
    def get(self, request):
        form = AuthenticationForm()

        context = {
            "form": form
        }
        return render(request, 'login/login.html', context)
    
    #@method_decorator(authenticated_user)
    def post(self, request):
        form = AuthenticationForm(request, data = request.POST)
        
        errors = []
        for field, field_errors in form.errors.items():
            for error in field_errors:
                errors.append(f"{field.title()}: {error}")
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            remember_me = request.POST.get('remember_me')
            if remember_me:
                request.session['remember_me'] = True
            else:
                request.session.pop('remember_me', None)
            return HttpResponseRedirect('/')
        context = {
            "form": form,
            'errors': errors,
        }
        return render(request, 'login/login.html', context)

class CadastrarUser(View):
    def get(self, request):
        userForm = CustomUserCreationForm()
        defaultUserForm = DefaultUserForm()
        errors = []
        for form in [userForm, defaultUserForm]:
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(f"{field.title()}: {error}")
        context = {
                'defaultUserForm' : defaultUserForm,
                'userForm' : userForm,
                'errors' : errors
        }

        return render(request, 'cadastros/cadastro.html', context)
    def post(self, request):
            userForm = CustomUserCreationForm(request.POST)
            defaultUserForm = DefaultUserForm(request.POST)
            if userForm.is_valid() and defaultUserForm.is_valid():
                email = userForm.cleaned_data.get('email')
                if not email.endswith('@gmail.com'):
                    userForm.add_error('email', 'Por favor, insira um e-mail válido')
                else:
                    user = userForm.save(commit = False)
                    user.is_active = False
                    user.save()

                    defaultUser = defaultUserForm.save(commit= False)
                    defaultUser.fk_user = user
                    defaultUser.save()
                    #self._send_email_verification(user)
                    return HttpResponseRedirect('/home/')
            context = {
                'defaultUserForm' : defaultUserForm,
                'userForm' : userForm,
            }
            return render(request, 'cadastros/cadastro.html', context)