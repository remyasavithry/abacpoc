from django.conf.urls import url, include

from company.views import CompanyViewSet


from django.views.generic import TemplateView

urlpatterns = [
    url(r'^/create_company$', CompanyViewSet.as_view({'post': 'create_company'})),
    url(r'^/list_company$', CompanyViewSet.as_view({'get': 'get_company'})),
    url(r'^/list$', TemplateView.as_view(template_name="opportunities.html"), name="list_opportunity"),
    url(r'^/create$', TemplateView.as_view(template_name="create_opportunity.html"), name="create_opportunity"),
]
