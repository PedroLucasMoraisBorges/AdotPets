from django.urls import path
from . import views

urlpatterns = [
    path("Empresa/", views.HomeCompany.as_view(), name='homeCompany'),

    # Produtos
    path("cadastros/cadastroProduto", views.InsertProduct.as_view(), name="cadastroProduto"),
    path("produtos/", views.Loja.as_view(), name="produtos"),
    path("produtos/loja", views.verLoja, name="verLoja"),
    path("produto/<int:id>", views.VerProduto.as_view(), name="verProduto"),

    # Carrinho
    path('produtos/carrinho', views.ViewCart.as_view(), name='shoppingCart'),
    path('produtos/carrinho/del/<int:id>',views.DeleteItemCart.as_view(), name='deleteItemCart'),
    path('produtos/adicionarCarrinho/<int:id>', views.adcCartInstant, name='adicionarCarrinho'),

    # Pedidos
    path('pedidos/cliente', views.Pedidos.as_view(), name='pedidos'),
    path('pedidos/empresa',views.PedidosEmpresa.as_view(), name='pedidosEmpresa'),
    path('aceitarPedido/<int:id>',views.aceitarPedido, name='aceitarPedido'),
    path('pedidos/aceitarTodos/<int:id>', views.aceitarTodosPedidos, name='aceitarTodosPedidos'),
    path('pedidos/empresa/aceitos/', views.PedidosAceitosEmpresa.as_view(), name='pedidosAceitos'),
    path('pedidos/cancelarPedido/<int:id>', views.cancelarPedido, name='cancelarPedido'),
    path('pedidos/cancelarTodosPedidos/<int:id>', views.cancelarTodosPedidos, name='cancelarTodosPedidos'),
    path('pedidos/confirmarEnvio/<int:id>', views.ConfirmarEnvio, name='confirmarEnvio'),

    # Cupons
    path('pedidos/cupom/<int:id>', views.VerCupom.as_view(), name='verCupom'),
    path('pedidos/cupons', views.Cupons.as_view(), name='cupons'),

]