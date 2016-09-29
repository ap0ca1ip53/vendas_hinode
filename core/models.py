# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Produto(models.Model):
    GENERO = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('N', 'Não se aplica'),
    )
    codigo = models.IntegerField()
    codigo_barra = models.CharField(max_length=13)
    nome = models.CharField(max_length=40)
    genero = models.CharField(max_length=1, choices=GENERO)

    def __unicode__(self):
        return self.nome


class Estoque(models.Model):
    produto = models.ForeignKey(Produto)
    vendedor = models.ForeignKey(User)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    quantidade = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Estoque'

    def __unicode__(self):
        return self.produto.nome

    def incrementaEstoque(self, quantidade):
        self.quantidade = self.quantidade + quantidade
        self.save()

    def decrementaEstoque(self, quantidade):
        self.quantidade = self.quantidade - quantidade
        self.save()


class NotaDeEntrada(models.Model):
    dataDaCompra = models.DateField(verbose_name='Data da compra')
    valorDaNota = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Notas de entrada'


class ProdutosPorNota(models.Model):
    notaDeEntrada = models.ForeignKey(NotaDeEntrada)
    itemDoEstoque = models.ForeignKey(Estoque, verbose_name='Produto')
    quantidade = models.IntegerField()

    def save(self, *args, **kwargs):
        self.itemDoEstoque.incrementaEstoque(self.quantidade)
        super(ProdutosPorNota, self).save(*args, **kwargs)


class Cliente(models.Model):
    SEXO = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )
    nome = models.CharField(max_length=60)
    sexo = models.CharField(max_length=1, choices=SEXO)
    endereco = models.CharField(max_length=60)
    bairro = models.CharField(max_length=40)
    dt_nascimento = models.DateField()
    
    def __unicode__(self):
        return self.nome

class FormaDePagamento(models.Model):
    EH_PARCELADO = (
        (True, 'Sim'),
        (False, 'Não')
    )
    descricao = models.CharField(max_length=60)
    parcelado = models.BooleanField()
    percentualDaOperadora = models.DecimalField(max_digits=5, decimal_places=2)
    prazoParaRecebimento = models.IntegerField()


class Venda(models.Model):
    dataDaVenda = models.DateField(verbose_name='Data da compra')
    cliente = models.ForeignKey(Cliente)
    formaDePagamento = models.ForeignKey(FormaDePagamento)
    quantidadeDeParcelas = models.IntegerField()
    produtosPorVenda = models.ManyToManyField(Estoque, through='ProdutosPorVenda')

    @property
    def total_da_venda(self):
        total_da_venda = 0
        for p in self.produtosPorVenda.all():
            total_da_venda = total_da_venda + p.valorDeVenda

        return total_da_venda


class ProdutosPorVenda(models.Model):
    estoque = models.ForeignKey(Estoque)
    venda = models.ForeignKey(Venda)
    quantidade = models.IntegerField()
    desconto = models.DecimalField(max_digits=5, decimal_places=2)
    valorDeVenda = models.DecimalField(max_digits=12, decimal_places=2)

