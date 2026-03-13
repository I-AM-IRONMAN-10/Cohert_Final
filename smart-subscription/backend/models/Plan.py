from mongoengine import Document, StringField, FloatField, ListField, BooleanField

class Plan(Document):
    name = StringField(required=True)
    description = StringField()
    price = FloatField(required=True)
    duration = StringField(default='monthly')
    features = ListField(StringField(), default=list)
    isActive = BooleanField(default=True)

    meta = {'collection': 'plans'}
