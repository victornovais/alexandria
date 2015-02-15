from rest_framework import serializers, viewsets

from acervo.models import Livro


class LivroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Livro
        fields = ('url', 'isbn', 'nome', 'editora',)


class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
