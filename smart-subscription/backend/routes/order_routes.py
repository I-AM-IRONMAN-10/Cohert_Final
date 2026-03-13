from flask import Blueprint, request, jsonify, g
from middleware.auth_middleware import protect
from models.Order import Order
from models.OrderItem import OrderItem
from models.Inventory import Inventory

order_bp = Blueprint('orders', __name__)

@order_bp.route('/upcoming', methods=['GET'])
@protect
def get_upcoming_box():
    # Find the most recent pending order for the user
    order = Order.objects(user=g.user, packingStatus='pending').order_by('-createdAt').first()
    
    if not order:
        return jsonify({'message': 'No upcoming box found.'}), 404

    items = OrderItem.objects(order=order)
    
    # If no items exist, let's mock generate some (AI mock)
    if len(items) == 0:
        invs = Inventory.objects()
        if len(invs) > 0:
            import random
            selected = random.choices(invs, k=3)
            for inv in selected:
                OrderItem(order=order, product=inv).save()
            items = OrderItem.objects(order=order)

    return jsonify({
        'order': {
            '_id': str(order.id),
            'packingStatus': order.packingStatus
        },
        'items': [{
            '_id': str(item.id),
            'isSwapped': item.isSwapped,
            'product': {
                '_id': str(item.product.id),
                'productName': item.product.productName,
                'category': item.product.category
            } if item.product else None
        } for item in items]
    })

@order_bp.route('/upcoming/swap', methods=['POST'])
@protect
def swap_item():
    data = request.json
    try:
        item = OrderItem.objects(id=data.get('orderItemId')).first()
        if not item or str(item.order.user.id) != str(g.user.id):
            return jsonify({'message': 'Not found or unauthorized'}), 404
            
        if item.order.packingStatus != 'pending':
            return jsonify({'message': 'Too late to swap, box is packed'}), 400
            
        new_prod = Inventory.objects(id=data.get('newProductId')).first()
        if not new_prod or new_prod.quantity <= 0:
            return jsonify({'message': 'Product out of stock'}), 400

        item.originalProduct = item.product
        item.product = new_prod
        item.isSwapped = True
        item.save()
        
        # Mark order as customized
        item.order.isCustomized = True
        item.order.save()

        return jsonify({'message': 'Item swapped successfully'})

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@order_bp.route('/history', methods=['GET'])
@protect
def get_order_history():
    orders = Order.objects(user=g.user, packingStatus__ne='pending').order_by('-createdAt')
    return jsonify([{
        '_id': str(o.id),
        'packingStatus': o.packingStatus,
        'deliveryStatus': o.deliveryStatus,
        'trackingNumber': o.trackingNumber,
        'createdAt': o.createdAt
    } for o in orders])
