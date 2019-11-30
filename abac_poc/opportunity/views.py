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

class OpportunityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = OpportunitySerializer
    lookup_field = 'id'
    queryset = Opportunity.objects.all()


class OpportunityDetailViewSet(viewsets.GenericViewSet):

    def get_opportunity(self, request, opportunity_id):

        user = User.objects.get(id=request.data.get('user_id', ''))
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