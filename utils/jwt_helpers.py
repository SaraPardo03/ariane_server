import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from configs.config import config

import jwt
from datetime import datetime, timedelta

def generate_token(user_id):
  payload = {
    'sub': user_id,
    "iat": datetime.utcnow().timestamp(),
    'exp': datetime.utcnow() + timedelta(hours=24)
  }
  token = jwt.encode(payload, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
  return token

def decode_token(token):
  try:
      payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
      return payload
  except jwt.ExpiredSignatureError:
      return None  # Token expiré
  except jwt.InvalidTokenError:
      return None  # Token invalide
