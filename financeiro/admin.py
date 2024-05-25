from django.contrib import admin
from .models import Produto, Vendas, Compras

admin.site.register(Produto)
admin.site.register(Vendas)
admin.site.register(Compras)