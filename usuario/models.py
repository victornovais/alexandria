# coding=utf-8
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Usuario(models.Model):
    cpf = models.CharField('Matricula', primary_key=True, max_length=20)
    nome = models.CharField('Nome', max_length=255, unique=True)

    # Implementações feitas para usuar essa classe como default do Django para tratar usuarios
    is_active = models.BooleanField(default=True)
    REQUIRED_FIELDS = ['cpf']
    USERNAME_FIELD = 'nome'