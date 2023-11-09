from django.shortcuts import render, redirect, HttpResponse
from auth_user import *
from .models import *
from .forms import *

from pages.decorator import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from pages.utilits import *
from django.views import View


class Loja(View):
    def get(self, request):
        search = request.GET.get('Search') if request.GET.get('Search') != None else ''

        products = getAllProcuts(search)

        productsList = []
        for product in products:
            productInfo = getProductInfo(product)

            productsList.append({
                'product' : product,
                'productImg' : productInfo['img'],
                'divided' : productInfo['divided']
            })

        info = getDefaultUser(request.user) if getDefaultUser(request.user) != None else ''
        context = {
            'productsList' : productsList,
            'info' : info,
            'search' : search
        }

        return render(request, 'loja/produtos.html', context)
    
class VerProduto(View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        productImg = ProductImage.objects.get(fk_product = product)
        context = {
            'produto' : product,
            'productImg' : productImg,
            'info' : getDefaultUser(request.user)
        }
        return render(request, 'loja/product.html', context)
    
    def post(self, request, id):
        if request.user.is_authenticated:
            product = Product.objects.get(id = id)
            quantity = request.POST.get('quantity')
            ShoppingCart.objects.create(fk_product=product, fk_user=request.user, ammount=quantity)
            return redirect('produtos')
        else:
            return redirect('login')

def verProduto(request, id):
    var = Product.objects.filter(id=id)
    if var != None:
        return render(request, 'produtos/produto.html', {'produto' : var})
    else:
        return HttpResponse("Esse produto não existe! Var = %s" %var)


def verLoja(request):
    company = Company.objects.get(fk_user=request.user)
    products = Product.objects.filter(fk_company=company)
    
    productsList = []
    for product in products:
        productInfo = getProductInfo(product)

        productsList.append({
            'product' : product,
            'productImg' : productInfo['img'],
            'divided' : productInfo['divided']
        })
    
    context = {
        'info' : getCompany(request.user),
        'productsList' : productsList,
        'company' : company
    }
    return render(request, 'loja/loja.html', context)


class HomeCompany(View):
    @method_decorator(login_required)
    @method_decorator(companyRequired)
    def get(self, request):
        search = request.GET.get('Search') if request.GET.get('Search') != None else ''
        info = getCompany(request.user)
        pets = []

        for pet in getMyPets(request.user, search):
            imgs = ImagePet.objects.filter(fk_pet = pet)
            if getTestLostPets(pet) == False:
                pets.append(
                    {
                        'pet' : pet,
                        'imgs': imgs,
                        'type':'myPets'}
                    )
            else:
                pets.append(
                    {
                        'pet' : pet,
                        'imgs': imgs,
                        'type':'myLostPets'}
                    )
            
        context = {
            'info' : info,
            'products' : getCompanyProducts(info['company']),
            'pets' : pets
        }

        return render(request, 'company/homeCompany.html', context)


class InsertProduct(View):
    @method_decorator(companyRequired)
    @method_decorator(login_required)
    def get(self, request):
        productForm = ProductForm()
        imgForm = ProductImgForm()
        context = {
            'productForm' : productForm,
            'btn' : 'Cadastrar produto',
            'imgForm' : imgForm
        }
        return render(request, 'cadastros/cadastroProduto.html', context)
    
    def post(self, request):
        productForm = ProductForm(request.POST)
        imgForm = ProductImgForm(request.POST, request.FILES)
        company = Company.objects.get(fk_user = request.user)

        

        if productForm.is_valid() and imgForm.is_valid():
            product = productForm.save(commit=False)
            product.fk_company = company
            product.save()

            img = imgForm.save(commit=False)
            img.fk_product = product
            img.save()
            return redirect('verLoja')


# # def editarProduto(request, id):
# #     product = Product.objects.get(id=id)
# #     form = ProductForm(request.POST or None, instance=product)
# #     if form.is_valid():
# #         form.save()
# #         print("É válido e foi salvo.")
# #         return redirect(produtos)

#     return render(request, 'editarProduto.html', {'produto' : product, 'form' : form})


class ViewCart(View):
    def get(self, request):
        cartItens = ShoppingCart.objects.filter(fk_user=request.user)
        products = []
        

        for item in cartItens:
            productImg = ProductImage.objects.get(fk_product = item.fk_product)
            ammount = item.ammount

            product = {
                'product' : item.fk_product,
                'productImg' : productImg.img.url,
                'ammount' : ammount,
                'cartItem' : item
            }
            products.append(product)

        context = {
            'info' : getDefaultUser(request.user),
            'products' : products
        }
        return render(request, 'loja/carrinho.html', context)
    def post(self, request):
        cartItens = ShoppingCart.objects.filter(fk_user=request.user)
        quantity = [request.POST.get(f'quantity[{i.id}]') for i in cartItens]

        city = request.POST.get('city')
        road = request.POST.get('road')
        number = request.POST.get('number')
        complement = request.POST.get('complement') if request.POST.get('complement') != None else ''
        

        address = OrderAddress.objects.create(city=city, road=road, number=number, complement=complement)

        for i in range(0, len(cartItens), 1):
            cartItens[i].ammount = quantity[i]
            cartItens[i].save()

            OrderIten.objects.create(fk_product=cartItens[i].fk_product, fk_user=request.user, ammount=cartItens[i].ammount, fk_address = address)
            cartItens[i].delete()

    
class DeleteItemCart(View):
    def get(self, reuquest, id):
        cartItem = ShoppingCart.objects.get(id=id)
        cartItem.delete()
        return redirect('shoppingCart')
    
class Pedidos(View):
    def get(self, request):
        requests = OrderIten.objects.filter(fk_user=request.user)
        itens = []
        
        
        for ItemRequest in requests:
            valueTotal = ItemRequest.fk_product.value * ItemRequest.ammount
            valueTotal = "{:.2f}".format(valueTotal)
            itens.append({
                'order' : ItemRequest,
                'product' : ItemRequest.fk_product,
                'productImg' : ProductImage.objects.get(fk_product=ItemRequest.fk_product).img.url,
                'addres' : ItemRequest.fk_address,
                'valueTotal' : valueTotal
            })
        context = {
            'info' : getDefaultUser(request.user),
            'orderItens' : itens
        }

        return render(request, 'loja/pedidos.html', context)       

class PedidosEmpresa(View):
    def get(self, request):
        company = Company.objects.get(fk_user = request.user)
        orders = OrderIten.objects.filter(fk_product__fk_company = company)

        clientes = []
        productsOrders = []
        
        for order in orders:

            cliente = order.fk_user
            if cliente in clientes:
                pass
            else:
                clientes.append(cliente)
                products = []
                for teste in orders:
                    
                    if teste.fk_user == cliente:
                        if teste.sent == False:
                            valueTotal = teste.fk_product.value * teste.ammount
                            valueTotal = "{:.2f}".format(valueTotal)
                            products.append({
                                'order' : teste,
                                'product' : teste.fk_product,
                                'productImg' : ProductImage.objects.get(fk_product=teste.fk_product).img.url,
                                'address' : teste.fk_address,
                                'valueTotal' : valueTotal,
                                'telephone' : DefaultUser.objects.get(fk_user=teste.fk_user).telephone,
                                'clientImg' : ProfileImage.objects.get(fk_user=teste.fk_user).img.url
                            })
                productsOrders.append(products)

        # for order in productsOrders:
        #     for item in order:
        #         print(item['order'], item['order'].fk_user)
        
        context = {
            'orders' : productsOrders,
            'info' : getCompany(request.user)
        }
        return render(request, 'loja/pedidosEmpresa.html', context)
