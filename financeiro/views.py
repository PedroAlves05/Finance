from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Produtos, Vendas, Compras
from django.contrib import messages
from django.contrib.messages import constants


@login_required
def estoque(request):
    if request.method == "GET":
        usuario = request.user
        produtos = Produtos.objects.filter(usuario=usuario)
        return render(request, 'estoque.html', {'produtos': produtos})


def adicionar_estoque(request):
    if request.method == "GET":
        usuario = request.user
        produtos = Produtos.objects.filter(usuario=usuario)
        return render(request, 'adicionar_estoque.html', {'produtos': produtos})
    elif request.method == "POST":
        usuario = request.user
        if request.POST.get("produtos_existentes"):
            produto_id = request.POST.get("produtos_existentes")
            produto = Produtos.objects.get(usuario = usuario, id__in = produto_id)
            quantidade = request.POST.get("quantidade")
            produto.quantidade += quantidade
            produto.save()
        elif request.POST.get("novo_produto"):
            produto = request.POST.get("novo_produto")
            quantidade = request.POST.get("quantidade")
            produto = Produtos(
                usuario = usuario,
                produto = produto,
                quantidade = quantidade
            )
            produto.save()
        valor = request.POST.get("valor")
        nova_compra = Compras(
            usuario = usuario,
            produto = produto,
            quantidade = quantidade,
            preco = valor
        )
        nova_compra.save()
        messages.add_message(request, constants.SUCCESS, 'Nova compra registrada com sucesso!')
        return redirect("/financeiro/estoque/")


@login_required
def vendas(request):
    if request.method == "GET":
        usuario = request.user
        vendas = Vendas.objects.filter(usuario=usuario)
        return render(request, 'vendas.html', {'vendas' : vendas})


@login_required
def adicionar_vendas(request):
    if request.method == "GET":
        usuario = request.user
        produtos = Produtos.objects.filter(usuario=usuario)
        return render(request, 'adicionar_vendas.html', {'produtos': produtos})
    elif request.method == "POST":
        usuario = request.user
        produto_id = request.POST.get("produtos_existentes")
        produto_escolhido = Produtos.objects.get(usuario = usuario, id__in = produto_id)
        quantidade = request.POST.get("quantidade")
        valor = request.POST.get("valor")
        nova_venda = Vendas(
            usuario = request.user,
            produto = produto_escolhido,
            quantidade = quantidade,
            preco = valor
        )
        nova_venda.save()
        produto_escolhido.quantidade -= quantidade
        produto_escolhido.save()
        messages.add_message(request, constants.SUCCESS, 'Nova venda registrada com sucesso!')
        return redirect("/financeiro/vendas/")


@login_required
def relatorio(request):
    if request.method == "GET":
        usuario = request.user
        vendas = Vendas.objects.filter(usuario=usuario)
        compras = Compras.objects.filter(usuario=usuario)
        total = compras - vendas
        return render(request, 'relatorio.html', {'vendas' : vendas, 'compras' : compras, 'total':total})