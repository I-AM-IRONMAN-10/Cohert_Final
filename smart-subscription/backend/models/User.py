from mongoengine import Document, StringField, IntField, DateTimeField, ReferenceField
from datetime import datetime

class User(Document):
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(choices=('user', 'staff', 'admin'), default='user')
    referralCode = StringField(unique=True)
    referredBy = ReferenceField('User', null=True)
    totalRewardPoints = IntField(default=0)
    createdAt = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'users'}
