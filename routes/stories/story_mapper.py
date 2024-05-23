from .story import Story
from bson.objectid import ObjectId

def to_entity(story_data: dict) -> Story:
    """
    Convert a dictionary representation of a story to a Story object.

    Args:
        story_data (dict): The dictionary containing story data.

    Returns:
        Story: The Story object created from the provided data.
    """
    s = Story()
    s.title = story_data.get("title")
    s.summary = story_data.get("summary", "")
    s.created_at = story_data.get("createdAt", "")
    s.updated_at = story_data.get("updatedAt", "")
    s.total_characters = story_data.get("totalCharacters", 0)
    s.total_end = story_data.get("totalEnd", 0)
    s.total_pages = story_data.get("totalPages", 0)
    s.total_open_node = story_data.get("totalOpenNode", 0)

    if story_data.get("_id") and isinstance(story_data.get("_id"), ObjectId):
      s.id = str(story_data.get("_id"))

    if story_data.get("userId") and isinstance(story_data.get("userId"), ObjectId):
      s.user_id = str(story_data.get("userId"))
    if story_data.get("userId") and type(story_data.get("userId")) == str:
       s.user_id = story_data.get("userId") 
    
    return s

def to_dict(s: Story) -> dict:
    """
    Convert a Story object to a dictionary representation.

    Args:
        s (Story): The Story object to convert.

    Returns:
        dict: A dictionary containing the attributes of the Story object.
    """
    story_dict = {
      "createdAt": s.created_at,
      "updatedAt": s.updated_at,
      "totalCharacters": s.total_characters,
      "totalEnd":s.total_end,
      "totalPage": s.total_pages,
      "totalOpenNode": s.total_open_node,
      "title": s.title,
      "summary": s.summary,
    }
    if s.id:
      story_dict["id"] = str(s.id)
    if s.user_id:
      story_dict["userId"] = str(s.user_id)


    return story_dict