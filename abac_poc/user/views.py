#from django.contrib.auth.models import User
from rest_framework_mongoengine import viewsets
from user.serializers import UserSerializer
from user.models import User

from user.keycloak_service import KeycloakService


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = UserSerializer
    lookup_field = 'id'
    queryset = User.objects.all()
    authentication_classes = []
    permission_classes = []
    def get_queryset(self):
        return User.objects.all()

    def create(self, request, *args, **kwargs):

        keycloak = KeycloakService().create_user(request.data)
        data = super().create(request, *args, **kwargs)

        return data