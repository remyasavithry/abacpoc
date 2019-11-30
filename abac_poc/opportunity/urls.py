from django.conf.urls import url, include
from django.urls import include, path

from opportunity.views import OpportunityViewSet, OpportunityDetailViewSet



urlpatterns = [

url(r'^get_opportunity/(?P<opportunity_id>[a-f0-9]{24})/detail$', OpportunityDetailViewSet.as_view({'get': 'get_opportunity'})),

]