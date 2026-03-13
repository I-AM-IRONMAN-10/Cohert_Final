from flask import Blueprint, jsonify, g
from middleware.auth_middleware import protect
from models.Reward import Reward

reward_bp = Blueprint('rewards', __name__)

@reward_bp.route('/', methods=['GET'])
@protect
def get_reward_history():
    rewards = Reward.objects(user=g.user).order_by('-createdAt')
    return jsonify([{
        '_id': str(r.id),
        'points': r.points,
        'reason': r.reason,
        'createdAt': r.createdAt
    } for r in rewards])
