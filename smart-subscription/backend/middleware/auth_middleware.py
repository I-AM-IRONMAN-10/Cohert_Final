import jwt
from functools import wraps
from flask import request, jsonify, g
from models.User import User
from config import Config

def protect(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if auth header is present
        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]

        if not token:
            return jsonify({'message': 'Not authorized, no token'}), 401

        try:
            # Decode token
            decoded = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
            # Find user and attach to g
            user = User.objects(id=decoded['id']).first()
            if not user:
                return jsonify({'message': 'User not found'}), 401
            
            g.user = user
        except Exception as e:
            return jsonify({'message': 'Not authorized, token failed'}), 401

        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    @wraps(f)
    @protect
    def decorated(*args, **kwargs):
        if g.user and g.user.role == 'admin':
            return f(*args, **kwargs)
        else:
            return jsonify({'message': 'Not authorized as an admin'}), 403
            
    return decorated

def staff_required(f):
    @wraps(f)
    @protect
    def decorated(*args, **kwargs):
        if g.user and getattr(g.user, 'role', '') in ['admin', 'staff']:
            return f(*args, **kwargs)
        else:
            return jsonify({'message': 'Not authorized as staff'}), 403
            
    return decorated
