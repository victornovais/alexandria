# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='cpf',
            field=models.CharField(max_length=20, serialize=False, verbose_name=b'Matricula', primary_key=True),
            preserve_default=True,
        ),
    ]
