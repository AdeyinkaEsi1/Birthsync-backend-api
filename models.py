from mongoengine import Document, StringField, DateField

class Person(Document):
    name = StringField(max_length=50)
    birth_date = DateField
    extra_info = StringField(max_length=200, required=False)