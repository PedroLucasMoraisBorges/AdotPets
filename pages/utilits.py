from .models import *
from auth_user.models import *
from django.db.models import Q

def getUserType(user):
    try:
        defaultUser = DefaultUser.objects.get(fk_user=user)
        return "defaultUser"
    except DefaultUser.DoesNotExist:
        pass

    try:
        company = Company.objects.get(fk_user=user)
        return "company"
    except Company.DoesNotExist:
        pass

# Return pets for adoption
def getPetsAdot(request, search):
    # To a registered user
    if request.user.is_authenticated:
        pets = list(reversed(Pet.objects.filter(~Q(fk_user=request.user) and Q(adopted=False)).filter(Q(name__istartswith=search) or Q(breed__istartswith=search) or Q(sex__istartswith=search))))
    # To an anonymous user
    else:
        pets = list(reversed(Pet.objects.filter().filter(Q(name__istartswith=search) or Q(breed__istartswith=search) or Q(sex__istartswith=search))))

    for pet in pets:
        try:
            lostPet = LostPets.objects.get(Q(fk_pet = pet))
            pets.remove(lostPet.fk_pet)
        except:
            pass
    print(pets)
    return pets

# Returns user's pets
def getMyPets(user, search):
    pets = list(Pet.objects.filter(Q(fk_user=user) & Q(adopted=False)).filter(Q(name__istartswith=search) or Q(breed__istartswith=search) or Q(sex__istartswith=search)))

    for pet in pets:
        print(pet.fk_user)
        try:
            lostPet = LostPets.objects.get(Q(fk_pet = pet) and Q(found=True))
            pets.remove(lostPet.fk_pet)
        except:
            pass
    return pets

# Returns lost pets
def getLostPets(request, search):
    # To a registered user
    if request.user.is_authenticated:
        pets = reversed(LostPets.objects.filter(~Q(fk_pet__fk_user=request.user)).filter(Q(fk_pet__name__istartswith=search) and Q(fk_pet__breed__istartswith=search) and Q(fk_pet__sex__istartswith=search)))
    # To an anonymous user
    else:
        pets = reversed(LostPets.objects.filter().filter(Q(fk_pet__name__istartswith=search) and Q(fk_pet__breed__istartswith=search) and Q(fk_pet__sex__istartswith=search)))
    return pets

# Returns the user's favorite pets
def getFavoritePets(user, search):
    pets = reversed(Favorites.objects.filter(Q(fk_donee=user)).filter(Q(fk_pet__name__istartswith=search) or Q(fk_pet__breed__istartswith=search) and Q(fk_pet__sex__istartswith=search)))
    return pets

# Returns defaultUser information
def getDefaultUser(user):
    address = Address.objects.get(fk_user=user)
    defaultUser = DefaultUser.objects.get(fk_user=user)
    profileImage = ProfileImage.objects.filter(fk_user=user).first()
    notifications = Notification.objects.filter(fk_donor=user)

    pestCount = Pet.objects.filter(fk_user=user).count()
    favoritesPets = Favorites.objects.filter(fk_donee=user).count()
    adoptedPets = LogExit.objects.filter(fk_donee=user).count()

    user_list = {
        'user':user,
        'defaultUser':defaultUser,
        'profileImage':profileImage,
        'address':address,
        'petsCount':pestCount,
        'favoritePets':favoritesPets,
        'adoptedPets':adoptedPets,
        'notifications':notifications,
        }
    
    return user_list


def getUserContacts(request, pet):
    if getUserType(pet.fk_user) == "defaultUser":
        defaultUser = DefaultUser.objects.get(fk_user=pet.fk_user)
        contacts = {
            'email' : pet.fk_user.email,
            'tel' : defaultUser.telephone 
        }
    else:
        company = DefaultUser.objects.get(fk_user=pet.fk_user)
        contacts = {
            'email' : pet.fk_user.email,
            'tel' : company.telephone 
        }
    return contacts
    

def getTestFavoritePets(pet):
    try:
        test = Favorites.objects.get(fk_pet = pet)
        result = True
    except:
        result = False
    return result

def getTestLostPets(pet):
    try:
        test = LostPets.objects.get(fk_pet = pet)
        result = True
    except:
        result = False
    return result