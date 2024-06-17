from django.db import models
from django.contrib.auth.models import User

class Produtos(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=50)
    quantidade = models.IntegerField()

    def __str__(self):
        return self.nome
    

class Vendas(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    produto = models.ForeignKey(Produtos, on_delete=models.DO_NOTHING)
    quantidade = models.IntegerField()
    preco = models.FloatField()
    data = models.DateTimeField()

    def __str__(self):
        return f'{self.produto} - {self.quantidade}'

class Compras(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    produto = models.ForeignKey(Produtos, on_delete=models.DO_NOTHING)
    quantidade = models.IntegerField()
    preco = models.FloatField()
    data = models.DateTimeField()

    def __str__(self):
        return f'{self.produto} - {self.quantidade}'
    

class Contatos(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    fornecedor = models.CharField(max_length=50)
    produto = models.CharField(max_length=50)
    telefone = models.CharField(max_length=50)