import random
import string
import hashlib

from .users_repository import users_repository
from .user import User

class users_service:
  def __init__(self):
    self.repository = users_repository()
  
  def get_all(self) -> list[dict]:
    try:
      return self.repository.get_all()
    except Exception as e:
      raise Exception(f"Failed to fetch users: {e}") from e
  
  def check_password(self, u:User, password:str) -> bool:    
    h_pwd = hashlib.sha256((u.salt+password).encode("utf-8")).hexdigest()

    if u.password != h_pwd:
      return False
    
    return True
  
  def create_user(self, u: User) -> User:
    already_user = self.repository.get_user_by_email(u.email)
    if already_user:
      raise ValueError(f"User with email {u.email} already exist.")

    salt = "".join(random.sample(string.ascii_lowercase, 5))
    h_pwd = hashlib.sha256((salt+u.password).encode("utf-8")).hexdigest()
    u.password = h_pwd
    u.salt = salt
    return self.repository.create_user(u)
  
  
  def get_user_by_id(self, user_id:str) -> User:
    user = self.repository.get_user_by_id(user_id)
    if not user:
      raise ValueError(f"User with id {user_id} not found.")
    return user
  
  def get_user_by_email(self, email:str)->User:
    user = self.repository.get_user_by_email(email)
    return user
  
  def delete_user(self, user_id:str) -> bool:
    existing_user = self.repository.get_user_by_id(user_id)
    if not existing_user:
      raise ValueError(f"User with id {user_id} not found.")
    return self.repository.delete_user(user_id)
  
  def update_user(self, user_id: str, user_data: dict) -> User:
    existing_user = self.repository.get_user_by_id(user_id)
    if not existing_user:
      raise ValueError(f"User with id {user_id} not found.")
    
    existing_user.firstname = user_data.get('firstname', existing_user.firstname)
    existing_user.lastname = user_data.get('lastname', existing_user.lastname)
    existing_user.username = user_data.get('username', existing_user.username)
    existing_user.email = user_data.get('email', existing_user.email)
    existing_user.password = user_data.get('password', existing_user.password)
    existing_user.salt = user_data.get('salt', existing_user.salt)

    return self.repository.update_user(existing_user)
  
