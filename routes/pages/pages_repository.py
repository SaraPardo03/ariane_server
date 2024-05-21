import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from configs.config_database import mongodb_uri 

# Create a new client and connect to the server
client = MongoClient(mongodb_uri, server_api=ServerApi('1'))
db = client["ariane"]


class pages_repository:
  def __init__(self):
    pass
  
  def get_all(self, user_id:str, story_id:str) -> list[dict]:
    pass
