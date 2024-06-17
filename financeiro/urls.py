from django.urls import path
from . import views

urlpatterns = [
    path('estoque/', views.estoque, name="estoque"),
    path('vendas/', views.vendas, name="vendas"),
    path('relatorio/', views.relatorio, name="relatorio"),
    path('adicionar_vendas/', views.adicionar_vendas, name="adicionar_vendas"),
    path('adicionar_estoque/', views.adicionar_estoque, name="adicionar_estoque"),
    path('contatos/', views.contatos, name='contatos'),
    path('extrato/', views.extrato, name='extrato')
]