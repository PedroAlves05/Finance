from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('estoque/', views.estoque, name="estoque"),
    path('vendas/', views.vendas, name="vendas"),
    path('relatorio/', views.relatorio, name="relatorio"),
    path('adicionar_vendas/', views.adicionar_vendas, name="adicionar_vendas"),
    path('adicionar_estoque/', views.adicionar_estoque, name="adicionar_estoque"),
    path('contatos/', views.contatos, name='contatos'),
    path('extrato/', views.extrato, name='extrato'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('alterar_estoque/', views.alterar_estoque, name="alterar_estoque"),
]