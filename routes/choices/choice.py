class Choice:
  def __init__(self, id: str="", page_id: str="", send_to_page_id: str="", title: str="") -> None:
    self.id = id
    self.page_id = page_id
    self.send_to_page_id = send_to_page_id
    self.title = title
  
  def __repr__(self) -> str:
    return f"{self.id} => ({self.page_id} {self.send_to_page_id}, {self.title})"