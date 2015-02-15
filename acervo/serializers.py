# coding: utf-8
from rest_framework import serializers

from acervo.models import Livro


class LivroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Livro
        fields = ('url', 'isbn', 'nome', 'editora',)
