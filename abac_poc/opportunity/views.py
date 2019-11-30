from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import status

from rest_framework.response import Response
import json

from opportunity.models import Opportunity
from opportunity.serializers import OpportunitySerializer

class HTTPResponse(Response):
    """
    Custom response structure for api call responses.
    """
    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        if isinstance(data, str):
            self.data = json.loads(data)
        else:
            self.data = data

        super(HTTPResponse, self).__init__(data=self.data, status=status)


class OpportunityViewSet(viewsets.GenericViewSet):
    keycloak_scopes = {
        'GET': 'opportunity:view',
        'POST': 'opportunity:add',
        'PUT': 'opportunity:update',
        'DELETE': 'opportunity:delete'
    }
    serializer_class = OpportunitySerializer
    def get_opportunity(self, request):
        id = request.GET.get('id', '')
        if id:
            opportunity = Opportunity.objects.get(id=id)
            opportunity = [opportunity]
        else:
            opportunity = Opportunity.objects.all()
        opportunity = OpportunitySerializer(opportunity, many=True).data
        #return HTTPResponse(opportunity, status.HTTP_200_OK)
        return Response({'opportunities': opportunity}, template_name='opportunities.html')

    def create_opportunity(self, request):

        title = request.data.get('title', 'Test')
        description = request.data.get('description', '')
        author = request.user
        managed_by = request.user

        opportunity = Opportunity()
        opportunity.title = title
        opportunity.description = description
        opportunity.author = author
        opportunity.managed_by = managed_by
        opportunity.save()
        data = OpportunitySerializer(opportunity).data
        return HTTPResponse(opportunity, status.HTTP_200_OK)