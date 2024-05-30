class Page:
  def __init__(self, id: str="", story_id: str="", previous_page_id: str="", end:bool=False, first:bool=False, title:str="", text:str="", total_pages:int=0, total_characters:int=0, section:int=None) -> None:
    self.id = id
    self.story_id = story_id
    self.previous_page_id = previous_page_id
    self.end = end
    self.first = first
    self.title = title
    self.text = text
    self.total_characters = total_characters
    self.section = section
  
  def __repr__(self) -> str:
    return f"{self.id} => ({self.story_id} {self.title}, {self.text})"