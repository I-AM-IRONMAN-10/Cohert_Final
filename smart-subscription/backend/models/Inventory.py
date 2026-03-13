from mongoengine import Document, StringField, IntField, DateTimeField

class Inventory(Document):
    productName = StringField(required=True)
    category = StringField(required=True)
    quantity = IntField(default=0)
    price = IntField(default=0)
    reorderLevel = IntField(default=10)

    meta = {'collection': 'inventories'}
