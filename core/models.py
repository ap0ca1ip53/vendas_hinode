# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from datetime import date

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
    consultor = models.ForeignKey(User)
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
    estoque = models.ForeignKey(Estoque, verbose_name='Produto')
    quantidade = models.IntegerField()

    def save(self, *args, **kwargs):
        self.estoque.incrementaEstoque(self.quantidade)
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
    cidade = models.CharField(max_length=40)
    telefone = models.CharField(max_length=11)
    celular = models.CharField(max_length=11)
    dt_nascimento = models.DateField(null=True, blank=True, verbose_name='Data de Nascimento')
    
    def __unicode__(self):
        return self.nome

    @property
    def idade(self):
        today = date.today()
        try:
            birthday = self.dt_nascimento.replace(year=today.year)
        except ValueError:  # raised when birth date is February 29 and the current year is not a leap year
            birthday = self.dt_nascimento.replace(year=today.year, month=self.dt_nascimento.month + 1, day=1)
        if birthday > today:
            return today.year - self.dt_nascimento.year - 1
        else:
            return today.year - self.dt_nascimento.year


class FormaDePagamento(models.Model):
    descricao = models.CharField(max_length=60)
    quantidade_de_parcelas = models.IntegerField()
    percentual_operadora = models.DecimalField(max_digits=5, decimal_places=2)
    prazo_para_recebimento = models.IntegerField()

    def __unicode__(self):
        return self.descricao


class Venda(models.Model):
    dataDaVenda = models.DateField(verbose_name='Data da venda')
    cliente = models.ForeignKey(Cliente)
    produtosPorVenda = models.ManyToManyField(Estoque, through='ProdutosPorVenda')
    forma_de_pagamento = models.ForeignKey(FormaDePagamento)

    def __unicode__(self):
        return '%s - %s' % (self.cliente.nome, self.dataDaVenda)

    @property
    def total_da_venda(self):
        total_da_venda = 0
        for p in self.produtosPorVenda.all():
            vl_unitario = ProdutosPorVenda.objects.get(venda=self, estoque=p).valorDeVenda
            quantidade = ProdutosPorVenda.objects.get(venda=self, estoque=p).quantidade
            total_da_venda = total_da_venda + vl_unitario * quantidade

        return total_da_venda


class ProdutosPorVenda(models.Model):
    estoque = models.ForeignKey(Estoque)
    venda = models.ForeignKey(Venda)
    quantidade = models.IntegerField()
    valorDeVenda = models.DecimalField(max_digits=12, decimal_places=2)
    desconto = models.DecimalField(max_digits=5, decimal_places=2)

    def save(self, *args, **kwargs):
        self.estoque.decrementaEstoque(self.quantidade)
        super(ProdutosPorVenda, self).save(*args, **kwargs)

class Parcela(models.Model):
    venda = models.ForeignKey(Venda)
    valorDaParcela = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Valor da Parcela')
    valorPago = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name='Valor Pago')
    dataDeVencimento = models.DateField(verbose_name='Data de vencimento')
    dataDePagamento = models.DateField(null=True, blank=True, verbose_name='Data de pagamento')
