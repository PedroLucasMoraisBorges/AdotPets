from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(DefaultUser)
admin.site.register(Empresa)
admin.site.register(Endereco)
admin.site.register(LogEntrada)
admin.site.register(LogSaida)