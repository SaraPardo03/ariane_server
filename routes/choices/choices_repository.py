import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from configs.config_database import mongodb_uri 
from .choice import Choice
from .choice_mapper import to_entity, to_dict

# Create a new client and connect to the MongoDB server
client = MongoClient(mongodb_uri, server_api=ServerApi('1'))
db = client["ariane"]

class pages_repository:
  """
  Repository for managing choice.

  This repository provides methods for interacting with the database
  to perform CRUD (Create, Read, Update, Delete) operations on choice.
  """
  def __init__(self):
    """
    Initialize a new choices_repository object.

    This constructor creates an instance of MongoClient to connect to the MongoDB server
    and selects the database named "ariane".
    """
    self.collection = db["choices"]
  
  def get_all(self, page_id:str) -> list[Choice]:
    """
    Retrieve all choice associated with a page_id.

    Args:
        page_id (str): The identifier of the page whose choices are to be retrieved.

    Returns:
        list[Choice]: A list containing the Choices objects associated with the specified page.
    
    Raises:
        Exception: If an error occurs while retrieving the choice.
    """
    try:
      choices_collection = self.collection.find({"pageId": ObjectId(page_id)})
      return [to_entity(choice) for choice in choices_collection]
    except Exception as e:
      raise Exception(f"Failed to get choice: {e}") from e
  
  def delete_all(self, page_id:str) ->int:
    """
    Delete all choices associated with a page.

    Args:
        page_id (str): The identifier of the page.

    Returns:
        int: the number of choice deleted
    
    Raises:
        Exception: If an error occurs while deleting the choices.
    """
    try:
      result = self.collection.delete_many({"pageId": ObjectId(page_id)})
      return result.deleted_count
    except Exception as e:
      raise Exception(f"An error occurred while delete choices whit page_id {page_id}: {e}") from e
  
  def get_choice_by_id(self, choice_id:str) ->Choice:
    """
    Retrieve a choice by its identifier.

    Args:
        choice_id (str): The identifier of the choice to retrieve.

    Returns:
        Choice: The Choice object corresponding to the specified identifier.
    
    Raises:
        ValueError: If no choice is found with the specified identifier.
        Exception: If an error occurs while retrieving the choice.
    """
    try:
      choice = self.collection.find_one({"_id": ObjectId(choice_id)})
      if not choice:
        raise ValueError(f"choice not found.")
      return to_entity(choice)
    except Exception as e:
      raise Exception(f"An error occurred while geting choice whit the id {choice_id}: {e}") from e
  
  def delete_choice(self, choice_id:str) ->bool:
    """
    Delete a choice by its identifier.

    Args:
        choice_id (str): The identifier of the choice to delete.

    Returns:
        bool: True if the choice is successfully deleted, False otherwise.
    
    Raises:
        ValueError: If no choice is found with the specified identifier.
        Exception: If an error occurs while deleting the choice.
    """
    try:
      result = self.collection.delete_one({"_id": ObjectId(choice_id)})
      if result.deleted_count != 1:
        raise ValueError(f"choice not found.")
      return result.deleted_count == 1
    except Exception as e:
      raise Exception(f"An error occurred while delete choice whit id {choice_id}: {e}") from e
  
  def create_choice(self, c: Choice) -> Choice:
    """
    Create a new choice.

    Args:
        c (Choice): The Choice object containing the information of the new Choice to create.

    Returns:
        Choice: The created Choice object.
    
    Raises:
        ValueError: If any of the required values to create the choice is missing.
        Exception: If an error occurs while inserting the choice.
    """
    if not c.page_id :
      raise ValueError("Choice page_id cannot be empty.")
    if not c.send_to_page_id :
      raise ValueError("Choice send_to_page_id cannot be empty.")
    if not c.title :
      raise ValueError("Choice title cannot be empty.")
  
    choice_data = to_dict(c)
    choice_data["pageId"] = ObjectId(choice_data["pageId"])
    choice_data["sendToPageId"] = ObjectId(choice_data["sendToPageId"])

    try:
      result = self.collection.insert_one(choice_data)

      if result.inserted_id:
        c.id = str(result.inserted_id)
        return c
      else:
        raise Exception("Failed to insert choice")
      
    except Exception as e:
      raise Exception(f"An error occurred while creating the choice: {e}") from e
     
  def update_choice(self, choice: Choice) -> Choice:
    """
    Update an existing choice.

    Args:
        choice (choice): The Choice object containing the updated information of the choice.

    Returns:
        Choice: The updated Choice object.
    
    Raises:
        ValueError: If no choice is found with the specified identifier.
        Exception: If an error occurs while updating the choice.
    """
    if not choice.page_id :
      raise ValueError("Choice page_id cannot be empty.")
    if not choice.send_to_page_id :
      raise ValueError("Choice send_to_page_id cannot be empty.")
    if not choice.title :
      raise ValueError("Choice title cannot be empty.")
  
    choice_data = to_dict(choice)
    choice_data.pop("id")
    choice_data.pop("pageId")
    choice_data.pop("sendToPageId")
    try:
      result = self.collection.update_one(
        {"_id": ObjectId(choice.id)},
        {"$set": choice_data}
      )
      if result.modified_count == 0:
        raise Exception("Failed to update choice.")
      
      print("update repo", result)
      return choice
    except Exception as e:
      raise Exception(f"An error occurred while updating the choice whit id {choice.id}: {e}") from e
