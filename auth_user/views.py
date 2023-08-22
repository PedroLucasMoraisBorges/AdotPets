from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views import View
from .models import *
from .forms import *

# Create your views here.
class Login(View):
    def get(self, request):
            return render(request, 'login/login.html')

class CadastrarUser(View):
    def get(self, request):
        userForm = CustomUserCreationForm()
        errors = []
        for form in [userForm]:
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(f"{field.title()}: {error}")
        context = {
                'userForm' : userForm,
                'errors' : errors
        }

        return render(request, 'cadastros/cadastro.html', context)
    def post(self, request):
            userForm = CustomUserCreationForm(request.POST)
            if userForm.is_valid():
                email = userForm.cleaned_data.get('email')
                if not email.endswith(('@gmail.com')):
                    userForm.add_error('email', 'Por favor, insira um e-mail válido da instituição.')
                else:
                    user = userForm.save(commit = False)
                    user.is_active = False
                    user.save()
                    #self._send_email_verification(user)
                    return HttpResponseRedirect('/cadastros/confirmar-email/')
            context = {
                'userForm': userForm,
            }
            return render(request, 'Cadastrar/cadastrar.html', context)
      