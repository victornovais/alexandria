# coding: utf-8
from rest_framework import serializers, exceptions
from django.utils.translation import ugettext_lazy as _

from acervo.models import Emprestimo

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
    emprestimos = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = ('cpf', 'nome', 'emprestimos')

    def get_emprestimos(self, obj):
        emprestimos_abertos = obj.emprestimos.filter(status=Emprestimo.Status.Aberto)
        serializer = EmprestimoSerializer(emprestimos_abertos, context=self.context, many=True)
        return serializer.data