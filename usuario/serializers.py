# coding: utf-8
from rest_framework import serializers, exceptions
from django.utils.translation import ugettext_lazy as _

from acervo.serializers import EmprestimoSerializer

from usuario.models import Usuario


class AlexandriaTokenSerializer(serializers.Serializer):
    cpf = serializers.CharField()

    def validate(self, attrs):
        cpf = attrs.get('cpf')

        try:
            usuario = Usuario.objects.get(cpf=cpf)
        except Usuario.DoesNotExist:
            msg = _('Usuario inexistente')
            raise exceptions.ValidationError(msg)

        attrs['user'] = usuario
        return attrs


class UsuarioSerializer(serializers.ModelSerializer):
    emprestimos = EmprestimoSerializer(many=True, read_only=True)

    class Meta:
        model = Usuario
        fields = ('cpf', 'nome', 'emprestimos')