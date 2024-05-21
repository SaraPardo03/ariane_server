import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from configs.config_database import mongodb_uri 
from .user import User
from .user_mapper import to_entity, to_dict

# Create a new client and connect to the MongoDB server
client = MongoClient(mongodb_uri, server_api=ServerApi('1'))
db = client["ariane"]

class users_repository:
  def __init__(self):
    self.collection = db["users"]
  
  def get_all(self) -> list[User]:
    try:
      users_collection = self.collection.find({})
      return [to_entity(user) for user in users_collection]
    except Exception as e:
      raise Exception(f"Failed to get users: {e}") from e
  
  def get_user_by_id(self, user_id:str) -> User:
    try:
      user = self.collection.find_one({"_id": ObjectId(user_id)})
      if not user:
        raise ValueError(f"User not found.")
      return to_entity(user)
    except Exception as e:
      raise Exception(f"An error occurred while geting user whit the id {user_id}: {e}") from e
    
  def get_user_by_email(self, email:str) -> User:
    try:
      user = self.collection.find_one({"email": email})
      if not user:
        return None
      return to_entity(user)
    except Exception as e:
      raise Exception(f"An error occurred while geting user whit the email {email}: {e}") from e
  
  def delete_user(self, user_id:str) ->bool:
    try:
      result = self.collection.delete_one({"_id": ObjectId(user_id)})
      if result.deleted_count != 1:
        raise ValueError(f"user not found.")
      return result.deleted_count == 1
    except Exception as e:
      raise Exception(f"An error occurred while delete user whit id {user_id}: {e}") from e
  
  def create_user(self, u: User) -> User:
    if not u.email:
      raise ValueError("User email cannot be empty.")
    if not u.password :
      raise ValueError("User password cannot be empty.")
    
    user_data = to_dict(u)

    result = self.collection.insert_one(user_data)
    
    if result.inserted_id:
      u.id = str(result.inserted_id)
      return u
    else:
      raise Exception("Failed to insert user")
    
  def update_user(self, user: User) -> User:
    try:
      result = self.collection.update_one(
        {"_id": ObjectId(user.id)},
        {"$set": to_dict(user)}
      )
      if result.modified_count == 0:
        raise Exception("Failed to update user.")
      return user
    except Exception as e:
      raise Exception(f"An error occurred while updating the user whit id {user.id}: {e}") from e
