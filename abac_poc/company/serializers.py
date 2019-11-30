from rest_framework_mongoengine import serializers
from company.models import Company

class CompanySerializer(serializers.DocumentSerializer):

    class Meta:
        model = Company
        fields = '__all__'