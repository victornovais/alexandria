from rest_framework import viewsets

from acervo.models import Livro
from acervo.serializers import LivroSerializer


class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
