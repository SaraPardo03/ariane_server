class Story:
  def __init__(self, id: str="", user_id: str="", created_at:str="", updated_at:str="", total_characters:int=0, total_end:int=0, total_pages:int=0, total_open_node:int=0, title: str="", summary: str="") -> None:
    self.id = id
    self.user_id = user_id
    self.created_at = created_at
    self.updated_at = updated_at
    self.total_characters = total_characters
    self.total_end = total_end
    self.total_pages = total_pages
    self.total_open_node = total_open_node
    self.title = title
    self.summary = summary
  
  def __repr__(self) -> str:
    return f"{self.id} => ({self.title} {self.summary})"