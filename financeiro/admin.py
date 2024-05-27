from django.contrib import admin
from .models import Produtos, Vendas, Compras

admin.site.register(Produtos)
admin.site.register(Vendas)
admin.site.register(Compras)