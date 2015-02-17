# coding: utf-8
from rest_framework import serializers, exceptions
from django.utils.translation import ugettext_lazy as _

from usuario.models import Usuario


class AlexandriaTokenSerializer(serializers.Serializer):
    cpf = serializers.CharField()

    def validate(self, attrs):
        cpf = attrs.get('cpf')

        try:
            usuario = Usuario.objects.get(cpf=cpf)

            # TODO: validar se usuário pode pegar livros
        except Usuario.DoesNotExist:
            msg = _('Usuario inexistente')
            raise exceptions.ValidationError(msg)

        attrs['user'] = usuario
        return attrs