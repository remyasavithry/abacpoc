from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import status
from django.conf import settings
from django.shortcuts import redirect

from rest_framework.response import Response
import json

from company.models import Company
from company.serializers import CompanySerializer

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


class CompanyViewSet(viewsets.GenericViewSet):
    serializer_class = CompanySerializer

    def get_company(self, request):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        id = request.GET.get('id', '')
        if id:
            company = Company.objects.get(id=id)
            company = [company]
        else:
            company = Company.objects.all()
        company = CompanySerializer(company, many=True).data
        #return HTTPResponse(opportunity, status.HTTP_200_OK)
        return Response({'opportunities': company}, template_name='companies.html')

    def create_company(self, request):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        name = request.data.get('name', 'Test')
        company = Company()
        company.name = name
        company.save()
        data = CompanySerializer(company).data
        return HTTPResponse(data, status.HTTP_200_OK)