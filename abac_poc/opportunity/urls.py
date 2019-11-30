from django.conf.urls import url, include

from opportunity.views import OpportunityViewSet


from django.views.generic import TemplateView

urlpatterns = [
    url(r'^/create_opportunity$', OpportunityViewSet.as_view({'post': 'create_opportunity'})),
    url(r'^/list_opportunity$', OpportunityViewSet.as_view({'get': 'get_opportunity'})),
    url(r'^/list$', TemplateView.as_view(template_name="opportunities.html"), name="list_opportunity"),
    url(r'^/create$', TemplateView.as_view(template_name="create_opportunity.html"), name="create_opportunity"),
]
