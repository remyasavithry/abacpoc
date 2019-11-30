from django.contrib.auth.models import User, Group
from rest_framework_mongoengine import viewsets
from company.serializers import CompanySerializer
from company.models import Company

class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
