from mongoengine import Document, StringField, DateTimeField, ReferenceField, BooleanField
from datetime import datetime

class Subscription(Document):
    user = ReferenceField('User', required=True)
    plan = ReferenceField('Plan', required=True)
    razorpaySubscriptionId = StringField()
    status = StringField(choices=('active', 'paused', 'cancelled'), default='active')
    startDate = DateTimeField(default=datetime.utcnow)
    nextDeliveryDate = DateTimeField()
    isGift = BooleanField(default=False)
    giftReceiverEmail = StringField()

    meta = {'collection': 'subscriptions'}
