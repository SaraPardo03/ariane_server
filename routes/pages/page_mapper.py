import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from .page import Page
from bson.objectid import ObjectId
from routes.choices.choice_mapper import to_entity as choice_to_entity
from routes.choices.choice_mapper import to_dict as choice_to_dict
def to_entity(page_data: dict) -> Page:
    """
    Convert a dictionary representation of a page to a Page object.

    Args:
        page_data (dict): The dictionary containing page data.

    Returns:
        Page: The Page object created from the provided data.
    """
    p = Page()
    p.end = page_data.get("end", False)
    p.first = page_data.get("first", False)
    p.title = page_data.get("title")
    p.text = page_data.get("text", "")
    p.section = page_data.get("section", None)
    p.total_characters = page_data.get("totalCharacters", 0)
    p.choices=[choice_to_entity(choice) for choice in page_data.get('choices', [])]
    p.choice_title = page_data.get("choiceTitle", "")
    p.image = page_data.get("image", "")
    

    if page_data.get("_id") and isinstance(page_data.get("_id"), ObjectId):
      p.id = str(page_data.get("_id"))

    if page_data.get("storyId") and isinstance(page_data.get("storyId"), ObjectId):
      p.story_id = str(page_data.get("storyId"))
    if page_data.get("storyId") and type(page_data.get("storyId")) == str:
      p.story_id = page_data.get("storyId")

    if page_data.get("previousPageId") and isinstance(page_data.get("previousPageId"), ObjectId):
      p.previous_page_id = str(page_data.get("previousPageId"))
    if page_data.get("previousPageId") and type(page_data.get("previousPageId")) == str:
      p.previous_page_id  = page_data.get("previousPageId") 

    
    return p

def to_dict(p: Page) -> dict:
    """
    Convert a Page object to a dictionary representation.

    Args:
        p (Page): The Page object to convert.

    Returns:
        dict: A dictionary containing the attributes of the page object.
    """
    page_dict = {
      "end": p.end,
      "first": p.first,
      "title": p.title,
      "text": p.text,
      "section": p.section,
      "totalCharacters": p.total_characters,
      "choices" :[choice_to_dict(choice) for choice in p.choices],
      "choiceTitle" :p.choice_title,
      "image": p.image,
    }
    
    if p.id:
      page_dict["id"] = str(p.id)

    if p.story_id:
      page_dict["storyId"] = str(p.story_id)

    if p.previous_page_id:
      page_dict["previousPageId"] = str(p.previous_page_id)


    return page_dict