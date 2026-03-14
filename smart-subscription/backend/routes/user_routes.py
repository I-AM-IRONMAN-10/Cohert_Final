from flask import Blueprint, request, jsonify, g
from middleware.auth_middleware import protect
from models.Preference import Preference
from models.User import User

user_bp = Blueprint('users', __name__)

@user_bp.route('/profile', methods=['GET'])
@protect
def get_user_profile():
    user = g.user
    prefs = Preference.objects(user=user).first()
    
    return jsonify({
        '_id': str(user.id),
        'name': user.name,
        'email': user.email,
        'role': user.role,
        'totalRewardPoints': user.totalRewardPoints,
        'referralCode': user.referralCode,
        'preferences': {
            'favoriteCategories': prefs.favoriteCategories if prefs else [],
            'allergies': prefs.allergies if prefs else [],
            'spiceTolerance': prefs.spiceTolerance if prefs else 'None'
        }
    })

@user_bp.route('/preferences', methods=['PUT'])
@protect
def update_preferences():
    data = request.json
    try:
        prefs = Preference.objects(user=g.user).first()
        if not prefs:
            prefs = Preference(user=g.user)

        if 'favoriteCategories' in data:
            prefs.favoriteCategories = data['favoriteCategories']
        if 'allergies' in data:
            prefs.allergies = data['allergies']
        if 'spiceTolerance' in data:
            prefs.spiceTolerance = data['spiceTolerance']

        prefs.save()
        
        return jsonify({
            'favoriteCategories': prefs.favoriteCategories,
            'allergies': prefs.allergies,
            'spiceTolerance': prefs.spiceTolerance
        })
    except Exception as e:
        return jsonify({'message': str(e)}), 500
