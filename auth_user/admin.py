from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(DefaultUser)
admin.site.register(Company)
admin.site.register(Address)
admin.site.register(LogEntry)
admin.site.register(LogExit)
admin.site.register(ProfileImage)
