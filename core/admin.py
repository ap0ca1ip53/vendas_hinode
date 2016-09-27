# -*- encoding: utf-8 -*-

from django.contrib import admin
from core.models import Produto, Cliente, Estoque, NotaDeEntrada, ProdutosPorNota

class EstoqueAdmin(admin.ModelAdmin):
    fields = ('produto', 'valor', 'quantidade')
    list_display = ('produto', 'valor', 'quantidade', 'vendedor')

    def save_model(self, request, obj, form, change):
        obj.vendedor = request.user
        obj.save()

admin.site.register(Estoque, EstoqueAdmin)

class ProdutosPorNotaInline(admin.StackedInline):
    model = ProdutosPorNota
    can_delete = False

class NotaDeEntradaAdmin(admin.ModelAdmin):
    inlines = (ProdutosPorNotaInline, )


admin.site.register(NotaDeEntrada, NotaDeEntradaAdmin)
admin.site.register(Produto)
admin.site.register(Cliente)

# Register your models here.
