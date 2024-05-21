class User:
  def __init__(self, id: str="", firstname: str="", lastname: str="", username: str="", email: str="", password: str="", salt: str="") -> None:
    self.id = id
    self.firstname = firstname
    self.lastname = lastname
    self.username = username
    self.email = email
    self.password = password
    self.salt = salt

  
  def __repr__(self) -> str:
    return f"{self.id} => (password: {self.password} email: {self.email})"