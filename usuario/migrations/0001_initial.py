# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('cpf', models.IntegerField(serialize=False, verbose_name=b'Matricula', primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=255, verbose_name=b'Nome')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
