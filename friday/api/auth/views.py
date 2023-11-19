from django.contrib.auth import logout

from friday.api.responses import ErrorResponse
from friday.api.views import TokenAPIView, SessionAPIView
from friday.core.serializer import serialize_user

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from .forms import LoginForm


class Login(TokenAPIView):
    def post(self, request: Request) -> Response:
        form = LoginForm(data=request.data)
        if form.is_valid():
            form.login(request)
            data = {
                'status': 'ok',
                'user': serialize_user(form.user)
            }

            header = {
                'session_key': request.session.session_key,
            }
            return Response(data, status=status.HTTP_200_OK, headers=header)
        return ErrorResponse(form=form)


class Profile(SessionAPIView):
    def get(self, request: Request) -> Response:
        data = serialize_user(request.user)
        return Response(data=data, status=status.HTTP_200_OK)


class Logout(SessionAPIView):
    def post(self, request: Request) -> Response:
        logout(request)
        return Response({"status": "OK"}, status=status.HTTP_200_OK)
