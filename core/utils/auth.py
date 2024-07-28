from typing import Optional, Tuple

import jwt
from django.conf import settings
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from jwt import PyJWTError
from rest_framework import authentication, permissions

from core.exceptions import AppException


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Extract the JWT from the Authorization header
        scheme, param = self.get_authorization_scheme_param(
            request.headers.get("Authorization")
        )
        if not scheme or not param:
            raise AppException.UnauthorizedException(error_message="unauthenticated")
        if scheme != "Bearer":
            raise AppException.UnauthorizedException(
                error_message="invalid authentication scheme"
            )
        try:
            return self.decode_token(token=param)
        except PyJWTError as exc:
            raise AppException.BadRequestException(error_message=exc.args) from exc

    def get_authorization_scheme_param(
        self,
        authorization_header_value: Optional[str],
    ) -> Tuple[str, str]:
        if not authorization_header_value:
            return "", ""
        scheme, _, param = authorization_header_value.partition(" ")
        return scheme, param

    def decode_token(self, token: str):
        public_key = f"-----BEGIN PUBLIC KEY-----\n{''.join(settings.jwt_public_key.split())}\n-----END PUBLIC KEY-----"  # noqa
        payload: dict = jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=settings.JWT_ALGORITHMS,
            audience="account",
            issuer=f"{settings.KEYCLOAK_URI}/realms/{settings.KEYCLOAK_REALM}",
        )
        payload["user_id"] = payload.get("preferred_username")
        return payload


class BlocklistPermission(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        return False


class MyAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "core.auth.JWTAuthentication"  # full import path OR class ref
    name = "MyAuthentication"  # name used in the schema

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
        }
