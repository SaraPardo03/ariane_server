import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from configs.config_database import mongodb_uri 
from .page import Page
from .page_mapper import to_entity, to_dict

# Create a new client and connect to the MongoDB server
client = MongoClient(mongodb_uri, server_api=ServerApi('1'))
db = client["ariane"]

class pages_repository:
  """
  Repository for managing pages.

  This repository provides methods for interacting with the database
  to perform CRUD (Create, Read, Update, Delete) operations on pages.
  """
  def __init__(self):
    """
    Initialize a new pages_repository object.

    This constructor creates an instance of MongoClient to connect to the MongoDB server
    and selects the database named "ariane".
    """
    self.collection = db["pages"]
  
  def get_all(self, story_id:str) -> list[Page]:
    """
    Retrieve all pages associated with a story.

    Args:
        story_id (str): The identifier of the story whose pages are to be retrieved.

    Returns:
        list[Pages]: A list containing the Pages objects associated with the specified story.
    
    Raises:
        Exception: If an error occurs while retrieving the pages.
    """
    try:
      pages_collection = self.collection.find({"storyId": ObjectId(story_id)})
      return [to_entity(page) for page in pages_collection]
    except Exception as e:
      raise Exception(f"Failed to get pages: {e}") from e
  
  def delete_all(self, story_id:str) ->int:
    """
    Delete all pages associated with a story.

    Args:
        story_id (str): The identifier of the story.

    Returns:
        int: the number of pages deleted
    
    Raises:
        Exception: If an error occurs while deleting the pages.
    """
    try:
      result = self.collection.delete_many({"storyId": ObjectId(story_id)})
      return result.deleted_count
    except Exception as e:
      raise Exception(f"An error occurred while delete pages whit story_id {story_id}: {e}") from e
  
  def get_page_by_id(self, page_id:str) ->Page:
    """
    Retrieve a page by its identifier.

    Args:
        page_id (str): The identifier of the page to retrieve.

    Returns:
        Page: The Page object corresponding to the specified identifier.
    
    Raises:
        ValueError: If no page is found with the specified identifier.
        Exception: If an error occurs while retrieving the page.
    """
    try:
      page = self.collection.find_one({"_id": ObjectId(page_id)})
      if not page:
        raise ValueError(f"page not found.")
      return to_entity(page)
    except Exception as e:
      raise Exception(f"An error occurred while geting page whit the id {page_id}: {e}") from e
  
  def delete_page(self, page_id:str) ->bool:
    """
    Delete a page by its identifier.

    Args:
        page_id (str): The identifier of the page to delete.

    Returns:
        bool: True if the page is successfully deleted, False otherwise.
    
    Raises:
        ValueError: If no page is found with the specified identifier.
        Exception: If an error occurs while deleting the page.
    """
    try:
      result = self.collection.delete_one({"_id": ObjectId(page_id)})
      if result.deleted_count != 1:
        raise ValueError(f"page not found.")
      return result.deleted_count == 1
    except Exception as e:
      raise Exception(f"An error occurred while delete page whit id {page_id}: {e}") from e
  
  def create_page(self, p: Page) -> Page:
    """
    Create a new page.

    Args:
        p (Page): The Page object containing the information of the new page to create.

    Returns:
        Page: The created Page object.
    
    Raises:
        ValueError: If any of the required values to create the page is missing.
        Exception: If an error occurs while inserting the page.
    """
    if not p.story_id :
      raise ValueError("Page story_id cannot be empty.")
    if not p.title :
      raise ValueError("Page title cannot be empty.")
  
    page_data = to_dict(p)
    page_data["storyId"] = ObjectId(page_data["storyId"])
    try:
      result = self.collection.insert_one(page_data)

      if result.inserted_id:
        p.id = str(result.inserted_id)
        return p
      else:
        raise Exception("Failed to insert page")
      
    except Exception as e:
      raise Exception(f"An error occurred while creating the page: {e}") from e
     
  def update_page(self, page: Page) -> Page:
    """
    Update an existing page.

    Args:
        page (Page): The Page object containing the updated information of the page.

    Returns:
        Page: The updated Page object.
    
    Raises:
        ValueError: If no page is found with the specified identifier.
        Exception: If an error occurs while updating the page.
    """
    if not page.story_id :
      raise ValueError("Page story_id cannot be empty.")
    if not page.title :
      raise ValueError("Page title cannot be empty.")
  
    page_data = to_dict(page)
    page_data.pop("id")
    page_data.pop("storyId")
    try:
      result = self.collection.update_one(
        {"_id": ObjectId(page.id)},
        {"$set": page_data}
      )
      if result.modified_count == 0:
        raise Exception("Failed to update page.")
      
      print("update repo", result)
      return page
    except Exception as e:
      raise Exception(f"An error occurred while updating the page whit id {page.id}: {e}") from e
