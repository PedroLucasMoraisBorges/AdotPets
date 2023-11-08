from django.urls import path
from . import views

urlpatterns = [
    path("Empresa/", views.HomeCompany.as_view(), name='homeCompany'),
    path("cadastros/cadastroProduto", views.InsertProduct.as_view(), name="cadastroProduto"),
    # path("produtos/editarProduto/<int:id>", views.editarProduto, name="editarProduto"),
    path("produtos/", views.Loja.as_view(), name="produtos"),
    # path("produtos/produto/<int:id>", views.verProduto, name="verProduto"),
    path("produtos/loja", views.verLoja, name="verLoja"),
    path("produto/<int:id>", views.VerProduto.as_view(), name="verProduto"),
    path('produtos/carrinho', views.ViewCart.as_view(), name='shoppingCart'),
    path('produtos/carrinho/del/<int:id>',views.DeleteItemCart.as_view(), name='deleteItemCart'),
    path('pedidos/', views.Pedidos.as_view(), name='pedidos')

]