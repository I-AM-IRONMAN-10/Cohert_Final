from mongoengine import Document, StringField, DateTimeField, ReferenceField, BooleanField
from datetime import datetime

class Order(Document):
    user = ReferenceField('User', required=True)
    subscription = ReferenceField('Subscription')
    packingStatus = StringField(choices=('pending', 'packed', 'shipped'), default='pending')
    deliveryStatus = StringField(choices=('processing', 'out-for-delivery', 'delivered'), default='processing')
    trackingNumber = StringField()
    isCustomized = BooleanField(default=False)
    createdAt = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'orders'}
