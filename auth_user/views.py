from django.shortcuts import render
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