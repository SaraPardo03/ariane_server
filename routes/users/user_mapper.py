from .user import User
from bson.objectid import ObjectId

def to_entity(user_data: dict) -> User:
  u = User()

  u.user_name = user_data.get("userName")
  u.first_name = user_data.get("firstName")
  u.last_name = user_data.get("lastName")
  u.email = user_data.get("email")
  u.password = user_data.get("password")
  u.salt = user_data.get("salt")
  u.token = user_data.get("token")

  if user_data.get("_id") and isinstance(user_data.get("_id"), ObjectId):
    u.id = str(user_data.get("_id"))

  return u

def to_dict(u: User) -> dict:
  user_dict = {
    "userName": u.user_name, 
    "firstName": u.first_name, 
    "lastName": u.last_name,
    "email": u.email,
    "password": u.password,
    "salt": u.salt,
  }
  
  if u.token:
    user_dict["token"] = u.token
  if u.id:
    user_dict["id"] = str(u.id)

  return user_dict