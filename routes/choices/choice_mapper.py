from .choice import Choice
from bson.objectid import ObjectId

def to_entity(choice_data: dict) -> Choice:
    """
    Convert a dictionary representation of a choice to a Choice object.

    Args:
        choice_data (dict): The dictionary containing choice data.

    Returns:
        Choice: The Choice object created from the provided data.
    """
    c = Choice()
    c.title = choice_data.get("title")

    if choice_data.get("_id") and isinstance(choice_data.get("_id"), ObjectId):
      c.id = str(choice_data.get("_id"))

    if choice_data.get("pageId") and isinstance(choice_data.get("pageId"), ObjectId):
      c.page_id = str(choice_data.get("pageId"))
    if choice_data.get("pageId") and type(choice_data.get("pageId")) == str:
      c.page_id = choice_data.get("pageId")

    if choice_data.get("sendToPageId") and isinstance(choice_data.get("sendToPageId"), ObjectId):
      c.send_to_page_id = str(choice_data.get("sendToPageId"))
    if choice_data.get("sendToPageId") and type(choice_data.get("sendToPageId")) == str:
      c.send_to_page_id  = choice_data.get("sendToPageId") 
    
    return c

def to_dict(c: Choice) -> dict:
    """
    Convert a Choice object to a dictionary representation.

    Args:
        c (Choice): The Choice object to convert.

    Returns:
        dict: A dictionary containing the attributes of the choice object.
    """
    choice_dict = {
      "title": c.title,
    }

    if c.id:
      choice_dict["id"] = str(c.id)

    if c.page_id:
      choice_dict["pageId"] = str(c.page_id)

    if c.send_to_page_id:
      choice_dict["sendToPageId"] = str(c.send_to_page_id)

    return choice_dict