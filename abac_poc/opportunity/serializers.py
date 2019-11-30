from rest_framework_mongoengine import serializers
from opportunity.models import Opportunity

class OpportunitySerializer(serializers.DocumentSerializer):

    class Meta:
        model = Opportunity
        fields = '__all__'