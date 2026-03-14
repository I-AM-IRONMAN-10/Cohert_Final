from flask import Blueprint, request, jsonify
from middleware.auth_middleware import staff_required
from models.Order import Order

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/orders/pending', methods=['GET'])
@staff_required
def get_pending_orders():
    orders = Order.objects(packingStatus='pending').order_by('createdAt')
    result = []
    for o in orders:
        result.append({
            '_id': str(o.id),
            'user': {
                'name': o.user.name,
                'email': o.user.email
            } if o.user else None,
            'packingStatus': o.packingStatus,
            'deliveryStatus': o.deliveryStatus,
            'isCustomized': o.isCustomized,
            'createdAt': o.createdAt
        })
    return jsonify(result)

@staff_bp.route('/orders/<id>/pack', methods=['PUT'])
@staff_required
def pack_order(id):
    try:
        order = Order.objects(id=id).first()
        if not order:
            return jsonify({'message': 'Order not found'}), 404
            
        order.packingStatus = 'packed'
        order.save()
        return jsonify({'message': 'Order marked as packed'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@staff_bp.route('/orders/<id>/ship', methods=['PUT'])
@staff_required
def ship_order(id):
    data = request.json
    try:
        order = Order.objects(id=id).first()
        if not order:
            return jsonify({'message': 'Order not found'}), 404
            
        order.packingStatus = 'shipped'
        order.deliveryStatus = 'out-for-delivery'
        if data and 'trackingNumber' in data:
            order.trackingNumber = data['trackingNumber']
            
        order.save()
        return jsonify({'message': 'Order marked as shipped', 'trackingNumber': order.trackingNumber})
    except Exception as e:
        return jsonify({'message': str(e)}), 500
