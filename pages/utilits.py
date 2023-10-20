from .models import *
from auth_user.models import *
from django.db.models import Q

def getPetsAdot(request, search):
    if request.user.is_authenticated:
        pets = reversed(Pet.objects.filter(~Q(fk_user=request.user)).filter(Q(nome__istartswith=search) or Q(raca__istartswith=search) or Q(sexo__istartswith=search)))
    else:
        pets = reversed(Pet.objects.filter().filter(Q(nome__istartswith=search) or Q(raca__istartswith=search) or Q(sexo__istartswith=search)))
        
    return pets

def getMyPets(user, search):
    pets = Pet.objects.filter(Q(fk_user=user)).filter(Q(nome__istartswith=search) or Q(raca__istartswith=search) or Q(sexo__istartswith=search))
    print(pets)
    return pets

def getLostPets(request, search):
    if request.user.is_authenticated:
        pets = reversed(AnimaisPerdidos.objects.filter(~Q(fk_pet__fk_user=request.user)).filter(Q(fk_pet__nome__istartswith=search) and Q(fk_pet__raca__istartswith=search) and Q(fk_pet__sexo__istartswith=search)))
    else:
        pets = reversed(AnimaisPerdidos.objects.filter().filter(Q(fk_pet__nome__istartswith=search) and Q(fk_pet__raca__istartswith=search) and Q(fk_pet__sexo__istartswith=search)))
    return pets

def getFavoritePets(user, search):
    pets = reversed(Favoritos.objects.filter(Q(fk_donatario=user)).filter(Q(fk_pet__nome__istartswith=search) or Q(fk_pet__raca__istartswith=search) and Q(fk_pet__sexo__istartswith=search)))
    return pets

def getDefaultUser(user):
    endereco = Endereco.objects.get(fk_user=user)
    defaultUser = DefaultUser.objects.get(fk_user=user)
    profileImage = ProfileImage.objects.get(fk_user=user)

    pestCount = Pet.objects.filter(fk_user=user).count()
    favoritesPets = Favoritos.objects.filter(fk_donatario=user).count()
    adoptedPets = LogSaida.objects.filter(fk_donatario=user).count()

    user_list = {
        'user':user,
        'defaultUser':defaultUser,
        'profileImage':profileImage,
        'endereco':endereco,
        'petsCount':pestCount,
        'favoritePets':favoritesPets,
        'adoptedPets':adoptedPets
        }
    
    return user_list
    