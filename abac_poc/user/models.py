
from mongoengine import StringField, ReferenceField, Document, ListField
from company.models import Company


class User(Document):
    first_name = StringField(max_length=200)
    last_name = StringField(max_length=200)
    email = StringField(max_length=200)
    roles = StringField(max_length=200)
    company = ReferenceField(Company)
    username = StringField(max_length=200)
    password = StringField(max_length=200)


