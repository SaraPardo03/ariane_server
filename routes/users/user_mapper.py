from .user import User
from bson.objectid import ObjectId

def to_entity(user_data: dict) -> User:
  u = User()
  if user_data.get("_id"):
    u.id = str(user_data.get("_id"))

  u.username = user_data.get("username")
  u.firstname = user_data.get("firstname")
  u.lastname = user_data.get("lastname")
  u.email = user_data.get("email")
  u.password = user_data.get("password")
  u.salt = user_data.get("salt")
  return u

def to_dict(u: User) -> dict:
  user_dict = {
    "username": u.username, 
    "firstname": u.firstname, 
    "lastname": u.lastname,
    "email": u.email,
    "password": u.password,
    "salt": u.salt,
  }

  if u.id:
    user_dict["_id"] = ObjectId(u.id)

  return user_dict