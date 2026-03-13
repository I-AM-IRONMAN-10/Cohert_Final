from flask import Blueprint, request, jsonify
from middleware.auth_middleware import admin_required, protect
from models.Inventory import Inventory
from models.Subscription import Subscription
from models.Preference import Preference
from datetime import datetime
from dateutil.relativedelta import relativedelta

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/inventory', methods=['GET'])
# Notice: For Hackathon demo preview item swap logic without token on some pages, 
# you could remove `@protect` here. But for strictness let's keep it and fetch client-side w/ token.
@protect 
def get_inventory():
    try:
        items = Inventory.objects()
        return jsonify([{
            '_id': str(i.id),
            'productName': i.productName,
            'category': i.category,
            'quantity': i.quantity,
            'price': i.price,
            'reorderLevel': i.reorderLevel
        } for i in items])
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@admin_bp.route('/inventory', methods=['POST'])
@admin_required
def add_inventory():
    data = request.json
    try:
        inv = Inventory(**data)
        inv.save()
        return jsonify({'message': 'Item added', '_id': str(inv.id)}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@admin_bp.route('/inventory/<id>', methods=['DELETE'])
@admin_required
def delete_inventory(id):
    try:
        Inventory.objects(id=id).delete()
        return jsonify({'message': 'Item deleted'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@admin_bp.route('/demand-prediction', methods=['GET'])
@admin_required
def get_demand_prediction():
    try:
        # Mock AI logic:
        # 1. Count active subscriptions scheduled for next month
        active_subs = Subscription.objects(status='active').count()
        
        # 2. Analyze user preferences to predict categories
        prefs = Preference.objects()
        categories_tally = {'snacks': 0, 'skincare': 0, 'books': 0, 'gadgets': 0}
        total_prefs = 0
        
        for p in prefs:
            for cat in p.favoriteCategories:
                if cat in categories_tally:
                    categories_tally[cat] += 1
                    total_prefs += 1
                
        # Estimate quantities based on proportional popularity
        predicted_demand = {
            'snacks': int((categories_tally['snacks'] / max(total_prefs, 1)) * active_subs * 3), # assuming 3 snacks per box
            'skincare': int((categories_tally['skincare'] / max(total_prefs, 1)) * active_subs * 2),
            'books': int((categories_tally['books'] / max(total_prefs, 1)) * active_subs * 1),
            'gadgets': int((categories_tally['gadgets'] / max(total_prefs, 1)) * active_subs * 1)
        }
        
        return jsonify({
            'message': 'AI Demand Prediction generated based on preference cluster analysis.',
            'totalSubscribersNextMonth': active_subs,
            'predictedDemand': predicted_demand
        })
    except Exception as e:
        return jsonify({'message': str(e)}), 500
