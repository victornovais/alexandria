# coding: utf-8
from rest_framework import serializers

from acervo.models import Livro, Exemplar, Emprestimo


class LivroSerializer(serializers.ModelSerializer):

    class Meta:
        model = Livro


class ExemplarSerializer(serializers.ModelSerializer):
    livro = LivroSerializer(read_only=True)

    class Meta:
        model = Exemplar
        fields = ('numero', 'livro')


class EmprestimoSerializer(serializers.ModelSerializer):
    exemplar = ExemplarSerializer(read_only=True)

    class Meta:
        model = Emprestimo
        fields = ('url', 'status', 'data_emprestimo', 'data_devolucao', 'exemplar',)
