# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


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
    valor = models.FloatField()
    quantidade = models.IntegerField()

    def __unicode__(self):
        return self.produto.nome


class NotaDeEntrada(models.Model):
    dataDaCompra = models.DateField()
    valorDaNota = models.FloatField()


class ProdutosPorNota(models.Model):
    notaDeEntrada = models.ForeignKey(NotaDeEntrada)
    itemDoEstoque = models.ForeignKey(Estoque, verbose_name='Produto')
    quantidade = models.IntegerField()

    def save(self, *args, **kwargs):
        self.itemDoEstoque.quantidade = self.itemDoEstoque.quantidade + self.quantidade
        self.itemDoEstoque.save()

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