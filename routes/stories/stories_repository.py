import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from configs.config_database import mongodb_uri 
from .story import Story
from .story_mapper import to_entity, to_dict

# Create a new client and connect to the server
client = MongoClient(mongodb_uri, server_api=ServerApi('1'))
db = client["ariane"]

class stories_repository:
  def __init__(self):
    self.collection = db["stories"]
  
  def get_all(self, user_id:str) -> list[Story]:
   #return [to_entity(story) for stories in self.collection.find({"user_id":user_id})]
    stories_collection = self.collection.find({"user_id":user_id})
    stories= []
    for story in stories_collection:
      stories.append(to_entity(story))

    return stories
  
  def create_story(self, s: Story) -> Story:
    print("create_story")
    if not s.title:
      raise ValueError("Story title cannot be empty.")

    story_data = to_dict(s)
    print("story_data", story_data)

    result = self.collection.insert_one(story_data)
    print("result", result)
    if result.inserted_id:
        s.id = str(result.inserted_id)
        return s
    else:
        raise Exception("Failed to insert story")
