from .models import *
from auth_user.models import *
from django.db.models import Q
from store.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect


def getUserType(user):
    if DefaultUser.objects.filter(fk_user=user).exists():
        return 'defaultUser'
    elif Company.objects.filter(fk_user=user).exists():
        return 'company'
    else:
        return 'otherUser'

# Return pets for adoption
def getPetsAdot(request, search):
    # To a registered user
    if request.user.is_authenticated:
        pets = list(reversed(Pet.objects.filter(~Q(fk_user=request.user) & Q(adopted=False)).filter(Q(name__istartswith=search) or Q(breed__istartswith=search) or Q(sex__istartswith=search))))
    # To an anonymous user
    else:
        pets = list(reversed(Pet.objects.filter(adopted=False).filter(Q(name__istartswith=search) or Q(breed__istartswith=search) or Q(sex__istartswith=search))))

    for pet in pets:
        try:
            lostPet = LostPets.objects.get(Q(fk_pet = pet))
            pets.remove(lostPet.fk_pet)
        except:
            pass
    return pets

# Returns user's pets
def getMyPets(user, search):
    pets = list(Pet.objects.filter(Q(fk_user=user) & Q(adopted=False)).filter(Q(name__istartswith=search) or Q(breed__istartswith=search) or Q(sex__istartswith=search)))

    for pet in pets:
        try:
            lostPet = LostPets.objects.get(Q(fk_pet = pet) & Q(found=True))
            pets.remove(lostPet.fk_pet)
        except:
            pass
    return pets

# Returns lost pets
def getLostPets(request, search):
    # To a registered user
    

    if request.user.is_authenticated:
        pets = reversed(LostPets.objects.filter(~Q(fk_pet__fk_user=request.user) & Q(found=False)).filter(Q(fk_pet__name__istartswith=search) and Q(fk_pet__breed__istartswith=search) and Q(fk_pet__sex__istartswith=search)))
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
    if user.is_authenticated:
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
    else:
        user_list = None
    
    return user_list

def getCompany(user):
    address = Address.objects.get(fk_user = user)
    company = Company.objects.get(fk_user = user)
    profileImage = ProfileImage.objects.filter(fk_user = user).first()
    notifications = Notification.objects.filter(fk_donor = user)


    

    pestCount = Pet.objects.filter(fk_user=user).count()
    products = Product.objects.filter(fk_company=company).count()
    adoptedPets = LogExit.objects.filter(fk_donee=user).count()
    user_list = {
        'user':user,
        'company':company,
        'profileImage':profileImage,
        'address':address,
        'petsCount':pestCount,
        'products':products,
        'adoptedPets':adoptedPets,
        'notifications':notifications,
        }
    
    return user_list

def getCompanyProducts(company):
    products = Product.objects.filter(fk_company = company)
    return products


def getUserContacts(request, pet):
    if getUserType(pet.fk_user) == "defaultUser":
        info = DefaultUser.objects.get(fk_user=pet.fk_user)
        pass

        contacts = {
            'email' : pet.fk_user.email,
            'tel' : info.telephone 
        }
    else:
        company = Company.objects.get(fk_user=pet.fk_user)
        contacts = {
            'email' : pet.fk_user.email,
            'tel' : company.telephone 
        }
    return contacts

def getTestFavoritePets(pet, user):
    try:
        test = Favorites.objects.get(Q(fk_pet = pet) & Q(fk_donee=user))
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


def redirecionar_usuario(user):
    user_type = getUserType(user)
    if user_type == 'defaultUser':
        return redirect('home')
    elif user_type == 'company':
        return redirect('homeCompany')
    

def getAllProcuts(search):
    products = Product.objects.filter(Q(name__istartswith = search) | Q(category__istartswith = search))

    return products

def getProductInfo(product):
    img = ProductImage.objects.get(fk_product = product)

    divided = 0
    if product.divided:
        divided = "{:.2f}".format(product.value / product.divided)

    product.value = "{:.2f}".format(product.value)
    
    if product.discount:
        product.discount = "{:.2f}".format(product.discount)
    
    return {
        'product' : product,
        'img' : img,
        'divided' : divided
    }