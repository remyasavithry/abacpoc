import re
import logging
from django.conf import settings
from django.http.response import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from keycloak.realm import KeycloakRealm

from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotAuthenticated

import json

logger = logging.getLogger(__name__)


class KeycloakMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        """

        :param get_response:
        """
        self.get_response = get_response
        self.config = settings.KEYCLOAK_CONFIG

        # Read configurations
        try:
            self.server_url = self.config['KEYCLOAK_SERVER_URL']
            self.client_id = self.config['KEYCLOAK_CLIENT_ID']
            self.realm_name = self.config['KEYCLOAK_REALM']
        except KeyError as e:
            raise Exception("KEYCLOAK_SERVER_URL, KEYCLOAK_CLIENT_ID or KEYCLOAK_REALM not found.")

        self.client_secret_key = self.config.get('KEYCLOAK_CLIENT_SECRET_KEY', None)
        self.client_public_key = self.config.get('KEYCLOAK_CLIENT_PUBLIC_KEY', None)
        self.default_access = self.config.get('KEYCLOAK_DEFAULT_ACCESS', "DENY")
        self.method_validate_token = self.config.get('KEYCLOAK_METHOD_VALIDATE_TOKEN', "INTROSPECT")
        self.keycloak_authorization_config = self.config.get('KEYCLOAK_AUTHORIZATION_CONFIG', None)

        self.realm = KeycloakRealm(server_url=self.server_url, realm_name=self.realm_name)

        self.oidc_client = self.realm.open_id_connect(client_id=self.client_id,
                                            client_secret=self.client_secret_key)

    @property
    def keycloak(self):
        return self._keycloak

    @keycloak.setter
    def keycloak(self, value):
        self._keycloak = value

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    @property
    def server_url(self):
        return self._server_url

    @server_url.setter
    def server_url(self, value):
        self._server_url = value

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, value):
        self._client_id = value

    @property
    def client_secret_key(self):
        return self._client_secret_key

    @client_secret_key.setter
    def client_secret_key(self, value):
        self._client_secret_key = value

    @property
    def client_public_key(self):
        return self._client_public_key

    @client_public_key.setter
    def client_public_key(self, value):
        self._client_public_key = value

    @property
    def realm(self):
        return self._realm_name

    @realm.setter
    def realm(self, value):
        self._realm_name = value

    @property
    def keycloak_authorization_config(self):
        return self._keycloak_authorization_config

    @keycloak_authorization_config.setter
    def keycloak_authorization_config(self, value):
        self._keycloak_authorization_config = value

    @property
    def method_validate_token(self):
        return self._method_validate_token

    @method_validate_token.setter
    def method_validate_token(self, value):
        self._method_validate_token = value

    def get_access_token(self):
        return self.oidc_client.client_credentials()

    def __call__(self, request):
        """

        :param request:
        :return:
        """
        return self.get_response(request)



    def process_view(self, request, view_func, view_args, view_kwargs):
        """

        Validate only the token introspect.

        :param request: django request
        :param view_func:
        :param view_args: view args
        :param view_kwargs: view kwargs
        :return:
        """

        if hasattr(settings, 'KEYCLOAK_BEARER_AUTHENTICATION_EXEMPT_PATHS'):
            path = request.path_info.lstrip('/')

            if any(re.match(m, path) for m in
                   settings.KEYCLOAK_BEARER_AUTHENTICATION_EXEMPT_PATHS):
                logger.debug('** exclude path found, skipping')
                return None

        try:
            view_scopes = view_func.cls.keycloak_scopes
        except AttributeError as e:
            logger.debug(
                'Allowing free acesss, since no authorization configuration (keycloak_scopes) found for this request route :%s',
                request)
            return None

        if 'HTTP_AUTHORIZATION' not in request.META:
            return JsonResponse({"detail": NotAuthenticated.default_detail},
                                status=NotAuthenticated.status_code)

        auth_header = request.META.get('HTTP_AUTHORIZATION').split()
        token = auth_header[1] if len(auth_header) == 2 else auth_header[0]

        # Get default if method is not defined.
        required_scope = view_scopes.get(request.method, None) \
            if view_scopes.get(request.method, None) else view_scopes.get('DEFAULT', None)

        # DEFAULT scope not found and DEFAULT_ACCESS is DENY
        if not required_scope and self.default_access == 'DENY':
            return JsonResponse({"detail": PermissionDenied.default_detail},
                                status=PermissionDenied.status_code)

        try:
            user_permissions = self.keycloak.get_permissions(token,
                                                             method_token_info=self.method_validate_token.lower(),
                                                             key=self.client_public_key)
        except KeycloakInvalidTokenError as e:
            return JsonResponse({"detail": AuthenticationFailed.default_detail},
                                status=AuthenticationFailed.status_code)

        for perm in user_permissions:
            if required_scope in perm.scopes:
                return None

        # User Permission Denied
        return JsonResponse({"detail": PermissionDenied.default_detail},
                            status=PermissionDenied.status_code)