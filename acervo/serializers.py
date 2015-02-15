# coding: utf-8
from rest_framework import serializers

from acervo.models import Livro, Exemplar


class ExemplarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exemplar
        fields = ('numero',)


class LivroSerializer(serializers.HyperlinkedModelSerializer):
    exemplares = ExemplarSerializer(many=True, read_only=True)

    class Meta:
        model = Livro
        fields = ('url', 'isbn', 'nome', 'editora', 'exemplares')