#from django.contrib.auth.models import User
from rest_framework_mongoengine import viewsets
from opportunity.serializers import OpportunitySerializer
from opportunity.models import Opportunity
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializer
from authz.services import OPAAuthService
from rest_framework.exceptions import PermissionDenied

from user.keycloak_service import KeycloakService

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class OpportunityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = OpportunitySerializer
    lookup_field = 'id'
    queryset = Opportunity.objects.all()
    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):

        res = super().create(request, *args, **kwargs)
        resource = {
            'id': res.data.get('id', ''),
            'name': res.data.get('title', ''),
            'type': 'opportunity'
        }
        keycloak = KeycloakService().create_resource_set(resource)
        opp = Opportunity.objects.get(id=res.data.get('id', ''))
        opp.resource_id = keycloak.get('_id', '')
        opp.save()
        return res


class OpportunityDetailViewSet(viewsets.GenericViewSet):
    authentication_classes = []
    permission_classes = []
    def get_opportunity(self, request, opportunity_id):

        user = User.objects.get(id=request.data.get('user_id', ''))
        #entitlement = KeycloakService().get_user_entitlement(user)
        permissions = KeycloakService().get_user_permission(user)
        user = UserSerializer(user).data
        opp = Opportunity.objects.get(id=opportunity_id)
        data = OpportunitySerializer(opp).data
        resource = data
        resource["type"] = "opportunity"
        permitted = OPAAuthService.request_auth(user, data, "view")
        if permitted:
            return Response(data)
        else:
            raise PermissionDenied