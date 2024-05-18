import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from configs.config_database import mongodb_uri 
from .story import Story
from .story_mapper import to_entity, to_dict

# Create a new client and connect to the MongoDB server
client = MongoClient(mongodb_uri, server_api=ServerApi('1'))
db = client["ariane"]

class stories_repository:
  """
  Repository for managing stories.

  This repository provides methods for interacting with the database
  to perform CRUD (Create, Read, Update, Delete) operations on stories.
  """
  def __init__(self):
    """
    Initialize a new stories_repository object.

    This constructor creates an instance of MongoClient to connect to the MongoDB server
    and selects the database named "ariane".
    """
    self.collection = db["stories"]
  
  def get_all(self, user_id:str) -> list[Story]:
    """
    Retrieve all stories associated with a user.

    Args:
        user_id (str): The identifier of the user whose stories are to be retrieved.

    Returns:
        list[Story]: A list containing the Story objects associated with the specified user.
    
    Raises:
        Exception: If an error occurs while retrieving the stories.
    """
    try:
      stories_collection = self.collection.find({"user_id": user_id})
      return [to_entity(story) for story in stories_collection]
    except Exception as e:
      raise Exception(f"Failed to get stories: {e}") from e
  
  def get_story_by_id(self, story_id:str) ->Story:
    """
    Retrieve a story by its identifier.

    Args:
        story_id (str): The identifier of the story to retrieve.

    Returns:
        Story: The Story object corresponding to the specified identifier.
    
    Raises:
        ValueError: If no story is found with the specified identifier.
        Exception: If an error occurs while retrieving the story.
    """
    try:
      story = self.collection.find_one({"_id": ObjectId(story_id)})
      if not story:
        raise ValueError(f"story not found.")
      return to_entity(story)
    except Exception as e:
      raise Exception(f"An error occurred while geting story whit the id {story_id}: {e}") from e
  
  def delete_story(self, story_id:str) ->bool:
    """
    Delete a story by its identifier.

    Args:
        story_id (str): The identifier of the story to delete.

    Returns:
        bool: True if the story is successfully deleted, False otherwise.
    
    Raises:
        ValueError: If no story is found with the specified identifier.
        Exception: If an error occurs while deleting the story.
    """
    try:
      result = self.collection.delete_one({"_id": ObjectId(story_id)})
      if result.deleted_count != 1:
        raise ValueError(f"story not found.")
      return result.deleted_count == 1
    except Exception as e:
      raise Exception(f"An error occurred while delete story whit id {story_id}: {e}") from e
  
  def create_story(self, s: Story) -> Story:
    """
    Create a new story.

    Args:
        s (Story): The Story object containing the information of the new story to create.

    Returns:
        Story: The created Story object.
    
    Raises:
        ValueError: If any of the required values to create the story is missing.
        Exception: If an error occurs while inserting the story.
    """
    if not s.user_id :
      raise ValueError("Story user_id cannot be empty.")
    if not s.title :
      raise ValueError("Story title cannot be empty.")
    
    story_data = to_dict(s)
    result = self.collection.insert_one(story_data)
    
    if result.inserted_id:
      s.id = str(result.inserted_id)
      return s
    else:
      raise Exception("Failed to insert story")
    
  def update_story(self, story: Story) -> Story:
    """
    Update an existing story.

    Args:
        story (Story): The Story object containing the updated information of the story.

    Returns:
        Story: The updated Story object.
    
    Raises:
        ValueError: If no story is found with the specified identifier.
        Exception: If an error occurs while updating the story.
    """
    try:
      result = self.collection.update_one(
        {"_id": ObjectId(story.id)},
        {"$set": to_dict(story)}
      )
      if result.modified_count == 0:
        raise Exception("Failed to update story.")
      return story
    except Exception as e:
      raise Exception(f"An error occurred while updating the story whit id {story.id}: {e}") from e
