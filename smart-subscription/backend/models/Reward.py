from mongoengine import Document, ReferenceField, IntField, StringField, DateTimeField
from datetime import datetime

class Reward(Document):
    user = ReferenceField('User', required=True)
    points = IntField(required=True)
    reason = StringField(required=True)
    createdAt = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'rewards'}
