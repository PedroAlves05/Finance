from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Produtos, Vendas, Compras


@login_required
def estoque(request):
    if request.method == "GET":
        usuario = request.user
        produtos = Produtos.objects.filter(usuario=usuario)
        return render(request, 'estoque.html', {'produtos': produtos})


@login_required
def vendas(request):
    if request.method == "GET":
        usuario = request.user
        vendas = Vendas.objects.filter(usuario=usuario)
        return render(request, 'vendas.html', {'vendas' : vendas})


@login_required
def relatorio(request):
    if request.method == "GET":
        usuario = request.user
        vendas = Vendas.objects.filter(usuario=usuario)
        compras = Compras.objects.filter(usuario=usuario)
        return render(request, 'relatorio.html', {'vendas' : vendas, 'compras' : compras})