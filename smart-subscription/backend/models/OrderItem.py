from mongoengine import Document, ReferenceField, BooleanField

class OrderItem(Document):
    order = ReferenceField('Order', required=True)
    product = ReferenceField('Inventory', required=True)
    isSwapped = BooleanField(default=False)
    originalProduct = ReferenceField('Inventory')

    meta = {'collection': 'order_items'}
