# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('acervo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emprestimo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_emprestimo', models.DateField(auto_now_add=True)),
                ('data_devolucao', models.DateField(null=True)),
                ('status', models.CharField(default=b'AB', max_length=2, choices=[(b'AB', b'Aberto'), (b'FE', b'Fechado'), (b'AT', b'Atrasado')])),
                ('exemplar', models.ForeignKey(to='acervo.Exemplar')),
                ('usuario', models.ForeignKey(related_name='emprestimos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'emprestimo',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelTable(
            name='exemplar',
            table='exemplar',
        ),
    ]
