# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-23 20:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60)),
                ('endereco', models.CharField(max_length=60)),
                ('bairro', models.CharField(max_length=40)),
                ('dt_nascimento', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField()),
                ('codigo_barra', models.CharField(max_length=13)),
                ('nome', models.CharField(max_length=40)),
                ('valor', models.FloatField()),
            ],
        ),
    ]
