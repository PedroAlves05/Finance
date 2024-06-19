from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Produtos, Vendas, Compras, Contatos
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime


@login_required
def estoque(request):
    if request.method == "GET":
        usuario = request.user
        produtos = Produtos.objects.filter(usuario=usuario)
        i = 0
        usuario1 = str(usuario)
        for letra in usuario1:
            if letra == '@':
                break
            i += 1
        nome_usuario = usuario1[0:i]

        return render(request, 'estoque.html', {'produtos': produtos, 'usuario': nome_usuario})
    elif request.method == "POST":
        usuario = request.user
        produto_escolhido = request.POST.get('filtrar_produto')
        compras = Compras.objects.filter(usuario=usuario, produto__nome=produto_escolhido)
        produtos = Produtos.objects.filter(usuario=usuario)
        i = 0
        for letra in usuario:
            if letra == '@':
                break
            i += 1
        nome_usuario = usuario[0:i]
        return render(request, 'vendas.html', {'compras' : compras, 'produtos': produtos, 'nome_usuario': nome_usuario})


def adicionar_estoque(request):
    if request.method == "GET":
        usuario = request.user
        produtos = Produtos.objects.filter(usuario=usuario)
        return render(request, 'adicionar_estoque.html', {'produtos': produtos})
    elif request.method == "POST":
        usuario = request.user
        produto = request.POST.get("produto")
        quantidade = request.POST.get("quantidade")
        produto = Produtos(
            usuario = usuario,
            nome = produto,
            quantidade = quantidade
        )
        produto.save()
        valor = request.POST.get("valor")
        nova_compra = Compras(
            usuario = usuario,
            produto = produto,
            quantidade = quantidade,
            preco = valor,
            data = datetime.now()
        )
        nova_compra.save()
        messages.add_message(request, constants.SUCCESS, 'Nova compra registrada com sucesso!')
        return redirect("/financeiro/estoque/")


@login_required
def vendas(request):
    if request.method == "GET":
        usuario = request.user
        vendas = Vendas.objects.filter(usuario=usuario)
        produtos = Produtos.objects.filter(usuario=usuario)
        i = 0
        usuario1 = str(usuario)
        for letra in usuario1:
            if letra == '@':
                break
            i += 1
        nome_usuario = usuario1[0:i]
        return render(request, 'vendas.html', {'vendas' : vendas, 'produtos': produtos, 'usuario': nome_usuario})
    elif request.method == "POST":
        usuario = request.user
        produto_escolhido = request.POST.get('filtrar_produto')
        vendas = Vendas.objects.filter(usuario=usuario, produto__nome=produto_escolhido)
        produtos = Produtos.objects.filter(usuario=usuario)
        i = 0
        usuario1 = str(usuario)
        for letra in usuario1:
            if letra == '@':
                break
            i += 1
        nome_usuario = usuario1[0:i]
        return render(request, 'vendas.html', {'vendas' : vendas, 'produtos': produtos, 'usuario': nome_usuario})


def adicionar_vendas(request):
    if request.method == "POST":
        usuario = request.user
        produto_id = request.POST.get("produtos_existentes")
        produto_escolhido = Produtos.objects.get(usuario = usuario, id__in = produto_id)
        quantidade = request.POST.get("quantidade")
        quantidade = int(quantidade)
        if produto_escolhido.quantidade < quantidade:
            messages.add_message(request, constants.ERROR, 'Não tem produtos o suficiente no estoque!')
            return redirect("/financeiro/vendas/")
        valor = request.POST.get("valor")
        nova_venda = Vendas(
            usuario = request.user,
            produto = produto_escolhido,
            quantidade = quantidade,
            preco = valor,
            data = datetime.now()
        )
        nova_venda.save()
        quantidade = int(quantidade)
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
        total_compras = 0
        total_vendas = 0
        for venda in vendas:
            total_vendas += venda.preco
        for compra in compras:
            total_compras += compra.preco
        total = total_vendas - total_compras
        return render(request, 'relatorio.html', {'total_vendas' : total_vendas, 'total_compras' : total_compras, 'total':total})

@login_required
def contatos(request):
    if request.method == "GET":
        usuario = request.user
        contatos = Contatos.objects.filter(usuario=usuario)
        return render(request, 'contatos.html', {'usuario': usuario, 'contatos': contatos})


@login_required
def extrato(request):
    usuario = request.user
    contatos = Contatos.objects.filter(usuario=usuario)
    return render(request, 'extrato.html', {'usuario': usuario})

def estoque1(request):
    if request.method == "GET":
        usuario = request.user
        produtos = Produtos.objects.filter(usuario=usuario)
        i = 0
        usuario1 = str(usuario)
        for letra in usuario1:
            if letra == '@':
                break
            i += 1
        nome_usuario = usuario1[0:i]

        return render(request, 'estoque1.html', {'produtos': produtos, 'usuario': nome_usuario})
    elif request.method == "POST":
        usuario = request.user
        produto_escolhido = request.POST.get('filtrar_produto')
        compras = Compras.objects.filter(usuario=usuario, produto__nome=produto_escolhido)
        produtos = Produtos.objects.filter(usuario=usuario)
        i = 0
        for letra in usuario:
            if letra == '@':
                break
            i += 1
        nome_usuario = usuario[0:i]
        return render(request, 'vendas.html', {'compras' : compras, 'produtos': produtos, 'nome_usuario': nome_usuario})