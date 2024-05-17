class Story:
  def __init__(self, id: str="", user_id: str="", title: str="", summary: str="") -> None:
    self.id = id
    self.user_id = user_id
    self.title = title
    self.summary = summary
  
  def __repr__(self) -> str:
    return f"{self.id} => ({self.title} {self.summary})"