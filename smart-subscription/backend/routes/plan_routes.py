from flask import Blueprint, jsonify
from models.Plan import Plan

plan_bp = Blueprint('plans', __name__)

@plan_bp.route('/', methods=['GET'])
def get_plans():
    try:
        plans = Plan.objects(isActive=True)
        # Seed logic if none exist (useful for hackathon demo)
        if len(plans) == 0:
            Plan(name="Starter AI Box", price=999, description="Curated essentials", duration="monthly").save()
            Plan(name="Premium AI Box", price=1999, description="Full premium items", duration="monthly").save()
            plans = Plan.objects(isActive=True)
            
        return jsonify([{
            '_id': str(p.id),
            'name': p.name,
            'price': p.price,
            'description': p.description,
            'duration': p.duration,
            'features': p.features
        } for p in plans])
    except Exception as e:
        return jsonify({'message': str(e)}), 500
