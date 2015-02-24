from datetime import timedelta, datetime
from rest_framework import viewsets, mixins
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from acervo.models import Emprestimo
from acervo.serializers import EmprestimoSerializer


class EmprestimoViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):

    serializer_class = EmprestimoSerializer
    queryset = Emprestimo.objects.all()

    def get_queryset(self):
        return super(EmprestimoViewSet, self).get_queryset().filter(usuario=self.request.user).exclude(status=Emprestimo.Status.Fechado)

    @detail_route(methods=['put'])
    def renovar(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.renovar()
        return Response(serializer.data)