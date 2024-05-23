class User:
  def __init__(self, id: str="", first_name: str="", last_name: str="", user_name: str="", email: str="", password: str="", salt: str="") -> None:
    self.id = id
    self.first_name = first_name
    self.last_name = last_name
    self.user_name = user_name
    self.email = email
    self.password = password
    self.salt = salt

  
  def __repr__(self) -> str:
    return f"{self.id} => (password: {self.password} email: {self.email})"