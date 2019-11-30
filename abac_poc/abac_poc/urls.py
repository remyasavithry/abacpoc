"""abac_poc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework import routers
from django.urls import path, include

#from opportunity.urls import urlpatterns
from user.views import UserViewSet
from company.views import CompanyViewSet
from opportunity.views import OpportunityViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, base_name='user-view')
router.register(r'company', CompanyViewSet, base_name='company-view')
router.register(r'opportunity', OpportunityViewSet, base_name='opportunity-view')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('opportunity.urls')),
]
