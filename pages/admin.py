from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Pet)
admin.site.register(ImagePet)
admin.site.register(LostPets)
admin.site.register(Favorites)
admin.site.register(Requests)
