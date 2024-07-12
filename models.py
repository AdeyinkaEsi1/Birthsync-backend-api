import datetime
from mongoengine import( 
    Document, 
    StringField, 
    DateTimeField,
    DateField)

class Person(Document):
    name = StringField(max_length=50, unique=True, required=True)
    birth_date = DateField(required=True)
    extra_info = StringField(max_length=200, required=True)
    

class BaseAccount(Document):
    username = StringField(max_length=50)
    email = StringField(max_length=50, unique=True, required=True)
    hashed_password = StringField(max_length=120, required=True)

