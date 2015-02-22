# coding: utf-8
from datetime import datetime, timedelta

from rest_framework import serializers

from acervo.models import Livro, Exemplar, Emprestimo


class LivroSerializer(serializers.ModelSerializer):

    class Meta:
        model = Livro


class ExemplarSerializer(serializers.ModelSerializer):
    livro = LivroSerializer(read_only=True)

    class Meta:
        model = Exemplar
        fields = ('id', 'numero', 'livro')


class EmprestimoSerializer(serializers.ModelSerializer):
    exemplar = ExemplarSerializer()

    class Meta:
        model = Emprestimo
        fields = ('url', 'status', 'data_emprestimo', 'data_devolucao', 'exemplar',)

    def create(self, validated_data):
        try:
            exemplar = Exemplar.objects.get(id=self.initial_data['exemplar']['id'])
        except Exemplar.DoesNotExist:
            raise serializers.ValidationError("Exemplar inexistente")

        if exemplar.emprestimo_set.exclude(status=Emprestimo.Status.Fechado).exists():
            raise serializers.ValidationError(u"Esse exemplar não está disponível para impréstimo")
        else:
            now = datetime.now()
            emprestimo = Emprestimo(
                exemplar=exemplar,
                usuario=self.context['request'].user,
                data_devolucao=now + timedelta(8),
                status=Emprestimo.Status.Aberto
            )
            emprestimo.save()
            return emprestimo