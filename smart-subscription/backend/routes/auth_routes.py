from flask import Blueprint, request, jsonify
from models.User import User
from models.Preference import Preference
from models.Reward import Reward
import bcrypt
import jwt
from config import Config

auth_bp = Blueprint('auth', __name__)

def generate_token(user_id):
    return jwt.encode({'id': str(user_id)}, Config.JWT_SECRET, algorithm="HS256")

@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.json
    try:
        if User.objects(email=data.get('email')).first():
            return jsonify({'message': 'User already exists'}), 400

        # Hash password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(data.get('password').encode('utf-8'), salt)

        # Handle referral
        referred_by_user = None
        ref_code = data.get('referralCode')
        if ref_code:
            referred_by_user = User.objects(referralCode=ref_code).first()

        # Generate unique referral code for new user
        import random
        import string
        new_ref_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

        user = User(
            name=data.get('name'),
            email=data.get('email'),
            password=hashed_password.decode('utf-8'),
            referralCode=new_ref_code,
            role='user'
        )

        if referred_by_user:
            user.referredBy = referred_by_user
            user.totalRewardPoints += 50
            referred_by_user.totalRewardPoints += 50
            referred_by_user.save()
            
            # Save rewards records
            Reward(user=user, points=50, reason='Signed up with referral').save()
            Reward(user=referred_by_user, points=50, reason='Referred a friend').save()

        user.save()
        
        # Initialize empty preferences
        Preference(user=user).save()

        return jsonify({
            '_id': str(user.id),
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'token': generate_token(user.id)
        }), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def auth_user():
    data = request.json
    try:
        user = User.objects(email=data.get('email')).first()
        
        if user and bcrypt.checkpw(data.get('password').encode('utf-8'), user.password.encode('utf-8')):
            return jsonify({
                '_id': str(user.id),
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'token': generate_token(user.id)
            })
        else:
            return jsonify({'message': 'Invalid email or password'}), 401

    except Exception as e:
        return jsonify({'message': str(e)}), 500
