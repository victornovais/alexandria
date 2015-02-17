from django.db import models
from rest_framework.authtoken.models import Token


class UsuarioManager(models.Manager):

    def create(self, cpf, nome):
        usuario = Usuario(cpf=cpf, nome=nome)
        usuario.save()

        Token.objects.create(user=usuario)


class Usuario(models.Model):
    cpf = models.IntegerField('Matricula', primary_key=True)
    nome = models.CharField('Nome', max_length=255, unique=True)

    objects = UsuarioManager()

    REQUIRED_FIELDS = ['cpf']
    USERNAME_FIELD = 'nome'