# coding: utf-8
from rest_framework import viewsets, mixins

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from usuario.models import Usuario

from usuario.serializers import AlexandriaTokenSerializer, UsuarioSerializer


class ObterAlexandriaToken(ObtainAuthToken):
    def post(self, request):
        serializer = AlexandriaTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class UsuarioViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()

    #TODO: garantir que o usuario só acessará o seu objeto
    # Tentei com get_queryset, mas não ficou legal