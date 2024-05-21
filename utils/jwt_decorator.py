import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from configs.config import config

from functools import wraps
from flask import request, jsonify
import jwt


def jwt_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    token = None

    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        token = auth_header.split(" ")[1] if auth_header.startswith('Bearer ') else None

    if not token:
        return jsonify({'message': 'Token is missing.'}), 401

    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        request.user_id = payload['sub']
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired. Please log in again.'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token. Please log in again.'}), 401

    return f(*args, **kwargs)

  return decorated_function
