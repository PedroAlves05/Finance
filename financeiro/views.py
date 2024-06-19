from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Produtos, Vendas, Compras, Contatos
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime
from django.utils.timezone import now


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
        i = 0
        usuario1 = str(usuario)
        for letra in usuario1:
            if letra == '@':
                break
            i += 1
        nome_usuario = usuario1[0:i]
        if request.POST.get('filtrar_produto'):
            produto_escolhido = request.POST.get('filtrar_produto')
            compras = Compras.objects.filter(usuario=usuario, produto__nome=produto_escolhido)
            produtos = Produtos.objects.filter(usuario=usuario)
            return render(request, 'vendas.html', {'compras' : compras, 'produtos': produtos, 'usuario': nome_usuario})
        if request.POST.get('alterar_produto'):
            produto_escolhido = request.POST.get('alterar_produto')
            produto = Produtos.objects.get(usuario=usuario, produto__id=produto_escolhido)

            return render(request, 'estoque.html', {'compras' : compras, 'produtos': produtos, 'usuario': nome_usuario, 'produto_escolhido': produto})
        return render(request, 'estoque.html')


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
        vendas = Vendas.objects.filter(usuario=usuario).order_by('-data')
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
        vendas = Vendas.objects.filter(usuario=usuario, produto__nome=produto_escolhido).order_by('-data')
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
        data_hoje = now()
        ano_atual = data_hoje.year
        mes_atual = data_hoje.month
        vendas = Vendas.objects.filter(usuario=usuario, data__year=ano_atual, data__month=mes_atual)
        compras = Compras.objects.filter(usuario=usuario, data__year=ano_atual, data__month=mes_atual)
        total_compras = 0
        total_vendas = 0
        for venda in vendas:
            total_vendas += venda.preco
        for compra in compras:
            total_compras += compra.preco
        total = total_vendas - total_compras
        i = 0
        usuario1 = str(usuario)
        for letra in usuario1:
            if letra == '@':
                break
            i += 1
        nome_usuario = usuario1[0:i]
        return render(request, 'relatorio.html', {'total_vendas' : total_vendas, 'total_compras' : total_compras, 'total':total, 'usuario': nome_usuario, 'ano': ano_atual, 'mes': mes_atual})

@login_required
def contatos(request):
    if request.method == "GET":
        usuario = request.user
        contatos = Contatos.objects.filter(usuario=usuario)
        return render(request, 'contatos.html', {'usuario': usuario, 'contatos': contatos})

from itertools import chain
from operator import attrgetter

@login_required
def extrato(request):
    usuario = request.user
    i = 0
    usuario1 = str(usuario)
    for letra in usuario1:
        if letra == '@':
            break
        i += 1
    nome_usuario = usuario1[0:i]
    usuario = request.user
    vendas = Vendas.objects.filter(usuario=usuario).order_by('-data')
    compras = Compras.objects.filter(usuario=usuario).order_by('-data')
    combined = chain(vendas, compras)
    result = sorted(combined, key=attrgetter('data'), reverse=True)
    produtos = Produtos.objects.filter(usuario=usuario)
    return render(request, 'extrato.html', {'usuario': nome_usuario, 'vendas': result, 'produtos': produtos})


@login_required
def alterar_estoque(request):
    if request.POST.get("produtos_existentes"):
        usuario = request.user
        produto_id = request.POST.get("produtos_existentes")
        produto = Produtos.objects.get(usuario = usuario, id = produto_id)
        quantidade = request.POST.get("quantidade")
        quantidade = int(quantidade)
        produto.quantidade += quantidade
        produto.save()
    return