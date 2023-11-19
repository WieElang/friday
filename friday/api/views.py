from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .authentication import SessionAuthentication, TokenAuthentication


class SessionAPIView(APIView):
    permission_classes: tuple = (IsAuthenticated,)
    authentication_classes: tuple = (SessionAuthentication,)


class TokenAPIView(APIView):
    authentication_classes: tuple = (TokenAuthentication,)
