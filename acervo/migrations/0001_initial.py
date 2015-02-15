# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exemplar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.IntegerField(default=1, verbose_name=b'Numero')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Livro',
            fields=[
                ('isbn', models.IntegerField(serialize=False, verbose_name=b'ISBN', primary_key=True)),
                ('nome', models.CharField(max_length=255, verbose_name=b'Nome')),
                ('editora', models.CharField(max_length=127, null=True, verbose_name=b'Editora', blank=True)),
            ],
            options={
                'db_table': 'livro',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='exemplar',
            name='livro',
            field=models.ForeignKey(related_name='exemplares', to='acervo.Livro'),
            preserve_default=True,
        ),
    ]
