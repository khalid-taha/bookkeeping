# modules/services/decorators.py

from functools import wraps
from flask import jsonify
from flask_login import current_user

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role not in roles:
                return jsonify({'error': 'Unauthorized access.'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator