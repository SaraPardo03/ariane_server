from .stories_repository import stories_repository
from .story import Story

class stories_service:
  def __init__(self):
    self.repository = stories_repository()
  
  def get_all(self) -> list[dict]:
    user_id = "1234567890"
    return self.repository.get_all(user_id)
  
  def create_story(self, s: Story) -> Story:
    return self.repository.create_story(s)
  
