from mongoengine import Document, ReferenceField, ListField, StringField

class Preference(Document):
    user = ReferenceField('User', required=True, unique=True)
    favoriteCategories = ListField(StringField(), default=list)
    allergies = ListField(StringField(), default=list)
    spiceTolerance = StringField(default='None')

    meta = {'collection': 'preferences'}
