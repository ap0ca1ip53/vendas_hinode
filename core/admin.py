# -*- encoding: utf-8 -*-

from django.contrib import admin
from core.models import Produto, Cliente, Estoque, NotaDeEntrada, ProdutosPorNota, ProdutosPorVenda, Venda, Parcela

class EstoqueAdmin(admin.ModelAdmin):
    fields = ('produto', 'valor', 'quantidade')
    list_display = ('produto', 'valor', 'quantidade', 'vendedor')

    def get_queryset(self, request):
        qs = super(EstoqueAdmin, self).get_queryset(request)
        qs = qs.filter(vendedor=request.user)

        return qs

    def save_model(self, request, obj, form, change):
        obj.vendedor = request.user
        obj.save()

admin.site.register(Estoque, EstoqueAdmin)

class ProdutosPorNotaInline(admin.TabularInline):
    model = ProdutosPorNota
    can_delete = False
    extra = 0
    verbose_name = 'produto'
    verbose_name_plural =  'produtos por nota'
    fieldsets = (
        (None, {'fields': ('itemDoEstoque', 'quantidade')}),
    )

class NotaDeEntradaAdmin(admin.ModelAdmin):
    list_display = ('id', 'dataDaCompra', 'valorDaNota')
    inlines = (ProdutosPorNotaInline, )

admin.site.register(NotaDeEntrada, NotaDeEntradaAdmin)

class ProdutosPorVendaInline(admin.TabularInline):
    model = ProdutosPorVenda
    extra = 0
    verbose_name_plural = 'Produtos'
    verbose_name = 'Produto'


class ParcelaInline(admin.TabularInline):
    model = Parcela
    extra = 1

class VendaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'dataDaVenda', 'total_da_venda')
    inlines = (ProdutosPorVendaInline, ParcelaInline)

admin.site.register(Venda, VendaAdmin)

class ParcelaAdmin(admin.ModelAdmin):
    list_display = ('venda', 'valorDaParcela', 'dataDeVencimento')

admin.site.register(Parcela, ParcelaAdmin)

class ClientelaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'endereco', 'dt_nascimento')
    list_display_links = ('nome',)

admin.site.register(Cliente, ClientelaAdmin)

admin.site.register(Produto)
# Register your models here.
