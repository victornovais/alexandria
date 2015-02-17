from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from usuario.serializers import AlexandriaTokenSerializer


class ObterAlexandriaToken(ObtainAuthToken):
    def post(self, request):
        serializer = AlexandriaTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})