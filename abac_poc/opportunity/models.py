from django.db import models

from user.models import User
from company.models import Company
from mongoengine import StringField, ReferenceField, Document


class Opportunity(Document):

    title = StringField(required=True, min_length=200)
    description = models.CharField(max_length=200)
    author = ReferenceField(User)
    managed_by = ReferenceField(User)
    company = ReferenceField(Company)
