# coding: utf-8
from rest_framework import serializers

from acervo.models import Livro, Exemplar


class LivroSerializer(serializers.HyperlinkedModelSerializer):
    exemplares = serializers.PrimaryKeyRelatedField(many=True, queryset=Exemplar.objects.all())

    class Meta:
        model = Livro
        fields = ('url', 'isbn', 'nome', 'editora', 'exemplares')
