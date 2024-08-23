from typing import Optional, Tuple

from django.conf import settings
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from jwt import PyJWTError
from keycloak import KeycloakOpenID
from rest_framework import permissions
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request

from core.exceptions import AppException


class KeycloakAuthentication(BaseAuthentication):
    def __init__(self):
        self.keycloak_openid = KeycloakOpenID(
            server_url=settings.KEYCLOAK_SERVER_URL,
            realm_name=settings.KEYCLOAK_REALM,
            client_id=settings.KEYCLOAK_CLIENT_ID,
            client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
        )
        super().__init__()

    def authenticate(self, request: Request):
        if "docs" in request.path or "schema" in request.path:
            return
        scheme, token = self.get_authorization_scheme(
            request.headers.get("Authorization")
        )
        if not (scheme and token):
            raise AppException.UnauthorizedException(error_message="unauthenticated")
        if scheme != "Bearer":
            raise AppException.UnauthorizedException(
                error_message="invalid authentication scheme"
            )
        try:
            account = self.keycloak_openid.decode_token(token)
            return account, None
        except PyJWTError as exc:
            raise AppException.BadRequestException(error_message=exc.args) from exc

    def get_authorization_scheme(
        self, authorization_value: Optional[str]
    ) -> Tuple[str, str]:
        if not authorization_value:
            return "", ""
        scheme, _, param = authorization_value.partition(" ")
        return scheme, param


class KeycloakAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "core.utils.auth.KeycloakAuthentication"
    name = "KeycloakAuthenticationScheme"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
        }


class BlocklistPermission(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        return False
