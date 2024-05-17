import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from config.config_database import mongodb_uri 

# Create a new client and connect to the server
client = MongoClient(mongodb_uri, server_api=ServerApi('1'))
db = client["ariane"]


class page_repository:
  def __init__(self):
    self.collection = db["pages"]
  
  def get_all(self, user_id:str, story_id:str) -> list[dict]:
    # Access the user's collection
    user_collection = self.collection[user_id]
    # Access the story collection within the user's collection
    story_collection = user_collection[story_id]
    # Retrieve pages in the story collection
    pages_collection = story_collection.find()
    print("poages:", story_collection.find())

    pages = []
    for page in pages_collection:
      print(page)
      #print("page:", type(page))
    return pages

#print(database.list_collection_names())


# Send a ping to confirm a successful connection
#try:
    #documents = collection.find()
    #for document in documents:
        #print(document)
    
    #client.admin.command('ping')
    #print("Pinged your deployment. You successfully connected to MongoDB!")
#except Exception as e:
    #print(e)
