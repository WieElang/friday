from typing import Optional, Tuple

from django.conf import settings
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, load_backend
from django.contrib.auth.models import AbstractBaseUser

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.request import Request


class TokenAuthentication(BaseAuthentication):
    token = 'ZnJpZGF5LXRhc2stbWFuYWdlbWVudC1hcHAtc3RhbXBzLWluZG9uZXNpYS0yMDIz='

    def authenticate(self, request: Request) -> None:
        supplied_token = None

        # Try to get token from Auth header
        auth_header = get_authorization_header(request).split()
        if auth_header and auth_header[0].lower() == b'token':
            if len(auth_header) == 1:
                msg = 'Invalid token header. No credentials provided.'
                raise exceptions.AuthenticationFailed(msg)
            elif len(auth_header) > 2:
                msg = 'Invalid token header. Token string should not contain spaces.'
                raise exceptions.AuthenticationFailed(msg)
            try:
                supplied_token = auth_header[1].decode()
            except UnicodeError:
                msg = 'Invalid token header. Token string should not contain invalid characters.'
                raise exceptions.AuthenticationFailed(msg)

        # Next attempt to get session key from body or query params
        if not supplied_token:
            supplied_token = request.data.get('token') or request.query_params.get('token')
            if not supplied_token:
                raise exceptions.AuthenticationFailed("Token isn't supplied")

            if supplied_token != self.token:
                raise exceptions.AuthenticationFailed("Invalid token")


class SessionAuthentication(BaseAuthentication):
    def authenticate(self, request: Request) -> Tuple[AbstractBaseUser, str]:
        session_key = None

        # Try to get session key from Auth header
        auth_header = get_authorization_header(request).split()
        if auth_header and auth_header[0].lower() == b'session':
            if len(auth_header) == 1:
                msg = 'Invalid token header. No credentials provided.'
                raise exceptions.AuthenticationFailed(msg)
            elif len(auth_header) > 2:
                msg = 'Invalid token header. Token string should not contain spaces.'
                raise exceptions.AuthenticationFailed(msg)
            try:
                session_key = auth_header[1].decode()
            except UnicodeError:
                msg = 'Invalid token header. Token string should not contain invalid characters.'
                raise exceptions.AuthenticationFailed(msg)

        # Next attempt to get session key from body or query params
        if not session_key:
            session_key = request.data.get('session_key') or request.query_params.get('session_key')
            if not session_key:
                raise exceptions.AuthenticationFailed("Session key isn't supplied")

        user = self.get_user(session_key)
        if user:
            return (user, session_key)

        raise exceptions.AuthenticationFailed('Invalid session id')

    def get_user(self, session_key: str) -> Optional[AbstractBaseUser]:
        '''
            Get user object from it's cached sessionid
            source : https://djangosnippets.org/snippets/1276/
        '''
        session_engine = __import__(settings.SESSION_ENGINE, {}, {}, [''])
        session_wrapper = session_engine.SessionStore(session_key)
        session = session_wrapper.load()
        user_id = session.get(SESSION_KEY)
        backend_id = session.get(BACKEND_SESSION_KEY)

        if user_id and backend_id:
            auth_backend = load_backend(backend_id)
            user = auth_backend.get_user(user_id)
            if user:
                return user

        return None
