from datetime import datetime, timedelta

from rest_framework import viewsets, mixins

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
        return super(EmprestimoViewSet, self).get_queryset().filter(usuario=self.request.user,
                                                                    status=Emprestimo.Status.Aberto)

    def perform_create(self, serializer):
        now = datetime.now()
        serializer.save(
            usuario=self.request.user,
            data_emprestimo=now,
            data_devolucao=now + timedelta(days=7),
            status=Emprestimo.Status.Aberto
        )