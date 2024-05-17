
from .pages_repository import page_repository

class page_service:
  def __init__(self):
    self.repository = page_repository()
  
  def get_all(self) -> list[dict]:
    user_id = "8IwwL9wW3ka6awFlmzA5ZjpezIs1"
    story_id = "-NrqOOgOun2GME8Iqbqy"

    return self.repository.get_all(user_id, story_id)
  
