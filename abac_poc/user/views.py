#from django.contrib.auth.models import User
from rest_framework_mongoengine import viewsets
from user.serializers import UserSerializer
from user.models import User


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = UserSerializer
    lookup_field = 'id'
    queryset = User.objects.all()

    def get_queryset(self):
        return User.objects.all()