from functools import wraps
import jwt
from flask import request, jsonify, g
from src.config import JWT_SECRET


def auth_required(f):
    """Verify JWT token and attach user info to Flask `g`."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'success': False, 'message': 'No token provided'}), 401
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            g.user_id = payload.get('userId')
            g.role    = payload.get('role')
            g.email   = payload.get('email')
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'message': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """Must be used AFTER @auth_required."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if getattr(g, 'role', None) != 'admin':
            return jsonify({'success': False, 'message': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated
