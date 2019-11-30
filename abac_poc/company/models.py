from django.db import models
from mongoengine import StringField, Document

class Company(Document):

    name = StringField(max_length=200)

