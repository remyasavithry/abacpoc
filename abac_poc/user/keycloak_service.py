
from keycloak.realm import KeycloakRealm
from django.conf import settings

class KeycloakService:

    admin_realm = KeycloakRealm(server_url=settings.KEYCLOAK_SETTINGS["server_url"],
                          realm_name=settings.KEYCLOAK_SETTINGS["admin_realm_name"])
    app_realm = KeycloakRealm(server_url=settings.KEYCLOAK_SETTINGS["server_url"],
                                realm_name=settings.KEYCLOAK_SETTINGS["app_realm_name"])
    admin_client = admin_realm.admin
    authz_client = app_realm.authz(client_id=settings.KEYCLOAK_SETTINGS['app_client_id'])
    uma_client = app_realm.uma()

    def get_admin_token(self):
        oidc_client = self.admin_realm.open_id_connect(client_id=settings.KEYCLOAK_SETTINGS['admin_client_id'],
                                            client_secret=settings.KEYCLOAK_SETTINGS['app_client_secret'])
        token = oidc_client.password_credentials('admin', 'admin')
        return token.get('access_token', '')

    def get_service_account_token(self):
        oidc_client = self.app_realm.open_id_connect(client_id=settings.KEYCLOAK_SETTINGS['app_client_id'],
                                                 client_secret=settings.KEYCLOAK_SETTINGS['app_client_secret'])
        token = oidc_client.client_credentials(client_id=settings.KEYCLOAK_SETTINGS['app_client_id'],
                                                 client_secret=settings.KEYCLOAK_SETTINGS['app_client_secret'])
        return token.get('access_token', '')

    def get_user_token(self, user):
        oidc_client = self.app_realm.open_id_connect(client_id=settings.KEYCLOAK_SETTINGS['app_client_id'],
                                            client_secret=settings.KEYCLOAK_SETTINGS['app_client_secret'])
        token = oidc_client.password_credentials(user.username, user.password)
        return token.get('access_token', '')

    def create_user(self, data):
        self.admin_client.set_token(self.get_admin_token())
        users = self.admin_client.realms.by_name('Demo').users
        username = data.get('username', 'username')
        details = {
            'credentials': {
                   "type": "password",
                   "value": data.get('password', ''),
                   "temporary": False
               },
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'email': data.get('email', ''),
            'enabled': True
        }
        data = users.create(username, **details)
        return data

    def get_user_entitlement(self, user):
        token = self.get_user_token(user)
        entitlement = self.authz_client.entitlement(token)
        return entitlement

    def get_user_permission(self, user):
        token = self.get_user_token(user)
        permission = self.authz_client.get_permissions(token)
        return permission

    def create_resource_set(self, resource):
        token = self.get_service_account_token()
        name = resource.get('id', '')
        rs_type = resource.get('type', '')
        res = self.uma_client.resource_set_create(token, name, type=rs_type)
        return res

