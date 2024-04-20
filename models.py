from mongoengine import( 
    Document, 
    StringField, 
    DateField)


class Person(Document):
    name = StringField(max_length=50, unique=True, required=True)
    birth_date = DateField(required=True)
    extra_info = StringField(max_length=200, required=True)