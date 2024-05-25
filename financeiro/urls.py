from django.urls import path
from . import views

urlpatterns = [
    path('estoque/', views.estoque, name="estoque"),
    path('vendas/', views.vendas, name="vendas"),
    path('relatorio/', views.relatorio, name="relatorio"),
]