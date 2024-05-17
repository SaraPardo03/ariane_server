class page:
  def __init__(self, id: str="", title: str="", text: str="", first: bool=0, end: bool=0, totalCharacters:int=0) -> None:
    self.id = id
    self.title = title
    self.text = text
    self.first = first
    self.end = end
    self.totalCharacters = totalCharacters
  
  def __repr__(self) -> str:
    return f"{self.id} => ({self.title} {self.text} {self.first} {self.end})"