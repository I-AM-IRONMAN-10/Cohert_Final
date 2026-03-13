from flask import Blueprint, request, jsonify, g
from middleware.auth_middleware import protect
from models.Plan import Plan
from models.Subscription import Subscription
from models.Reward import Reward
from config import razorpay_client
from datetime import datetime
from dateutil.relativedelta import relativedelta

subscription_bp = Blueprint('subscriptions', __name__)

@subscription_bp.route('/checkout', methods=['POST'])
@protect
def initiate_checkout():
    data = request.json
    try:
        plan = Plan.objects(id=data.get('planId')).first()
        if not plan:
            return jsonify({'message': 'Plan not found'}), 404

        order_amount = int(plan.price * 100)  # paise
        options = {
            'amount': order_amount,
            'currency': 'INR',
            'receipt': f"receipt_{g.user.id}"
        }
        
        # Razorpay integration
        razorpay_order = razorpay_client.order.create(data=options)
        
        return jsonify({
            'plan': {
                '_id': str(plan.id),
                'name': plan.name,
                'price': plan.price,
                'duration': plan.duration
            },
            'order': razorpay_order
        })

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@subscription_bp.route('/verify', methods=['POST'])
@protect
def verify_payment():
    data = request.json
    try:
        # In a real app we verify signature:
        # razorpay_client.utility.verify_payment_signature(data)

        plan = Plan.objects(id=data.get('planId')).first()
        
        # Calculate next delivery
        next_delivery = datetime.utcnow() + relativedelta(months=1) if plan.duration == 'monthly' else datetime.utcnow() + relativedelta(years=1)

        sub = Subscription(
            user=g.user,
            plan=plan,
            razorpaySubscriptionId=data.get('razorpay_subscription_id', 'mock_sub_id'),
            nextDeliveryDate=next_delivery,
            isGift=data.get('isGift', False),
            giftReceiverEmail=data.get('giftReceiverEmail', '')
        )
        sub.save()

        # Add rewards for purchasing subscription
        g.user.totalRewardPoints += 100
        g.user.save()
        Reward(user=g.user, points=100, reason=f"Subscribed to {plan.name}").save()

        # Also generate an initial dummy Order (Upcoming box) to populate immediately
        from models.Order import Order
        Order(user=g.user, subscription=sub).save()

        return jsonify({'message': 'Payment successful', 'subscriptionId': str(sub.id)})

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@subscription_bp.route('/', methods=['GET'])
@protect
def get_user_subscriptions():
    subs = Subscription.objects(user=g.user)
    result = []
    
    for sub in subs:
        result.append({
            '_id': str(sub.id),
            'status': sub.status,
            'plan': { 'name': sub.plan.name } if sub.plan else None,
            'nextDeliveryDate': sub.nextDeliveryDate,
            'isGift': sub.isGift,
            'giftReceiverEmail': sub.giftReceiverEmail
        })
    return jsonify(result)

@subscription_bp.route('/<sub_id>/pause', methods=['PUT'])
@protect
def pause_subscription(sub_id):
    try:
        sub = Subscription.objects(id=sub_id, user=g.user).first()
        if not sub:
            return jsonify({'message': 'Not found'}), 404
            
        sub.status = 'paused'
        sub.nextDeliveryDate = sub.nextDeliveryDate + relativedelta(months=1)
        sub.save()
        return jsonify({'message': 'Paused for 1 month'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@subscription_bp.route('/<sub_id>/cancel', methods=['PUT'])
@protect
def cancel_subscription(sub_id):
    try:
        sub = Subscription.objects(id=sub_id, user=g.user).first()
        if not sub:
            return jsonify({'message': 'Not found'}), 404
            
        sub.status = 'cancelled'
        sub.save()
        return jsonify({'message': 'Subscription cancelled'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500
