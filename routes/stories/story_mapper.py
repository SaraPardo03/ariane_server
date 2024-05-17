from .story import Story
from bson.objectid import ObjectId

def to_entity(story_data: dict) -> Story:
    print("to_entity", type(story_data))
    s = Story()
    s.id = str(story_data.get("_id"))
    s.user_id = story_data.get("user_id")
    s.title = story_data.get("title")
    s.summary = story_data.get("summary")
    return s

def to_dict(s: Story) -> dict:
    story_dict = {
        "user_id": s.user_id,
        "title": s.title,
        "summary": s.summary,
    }

    if s.id:
        story_dict["_id"] = ObjectId(s.id)

    return story_dict