from .choices_repository import choices_repository
from .choice import Choice

class choices_service:
  """
  Service for managing choice.

  This service acts as an interface between the API routes and the data repository
  to perform operations related to choice.
  """
  def __init__(self):
    """
    Initialize a new choices_service object.

    This constructor creates an instance of choice_repository to interact
    with the database.
    """
    self.repository = choices_repository()
  
  def get_all(self, page_id:str) -> list[dict]:
    """
    Retrieve all choice associated with a page_id.

    Args:
      page_id (str): The page identifier.

    Returns:
      list[dict]: A list containing the information of all the choice pages.
    
    Raises:
      Exception: If an error occurs while fetching the choices.
    """
    try:
      return self.repository.get_all(page_id)
    except Exception as e:
      raise Exception(f"Failed to fetch choices: {e}") from e
    
  def delete_all(self, page_id:str) -> int:
    """
    Delete all choices associated with a pages_id.

    Args:
      page_id (str): The page identifier.

    Returns:
      int: the number of choices deleted
    
    Raises:
      Exception: If an error occurs while deleting the choices.
    """
    try:
      return self.repository.delete_all(page_id)
    except Exception as e:
      raise Exception(f"Failed to delete choice: {e}") from e
  
  def create_choice(self, c: Choice) -> Choice:
    """
    Create a new choice.

    Args:
      c (Choice): The Choice object containing the information of the new choice.

    Returns:
      Choice: The created Choice object.

    Raises:
      ValueError: If any of the required values to create the choice is missing.
      Exception: If an error occurs while creating the choice.
    """
    try:
      return self.repository.create_choice(c)
    except ValueError as ve:
      raise ValueError(f"Missing required values to create the choice: {ve}") from ve
    except Exception as e:
      raise Exception(f"Failed to create choice: {e}") from e
    
  
  def get_choice_by_id(self, choice_id:str) -> Choice:
    """
    Retrieve a choice by its identifier.

    Args:
      choice_id (str): The identifier of the choice.

    Returns:
      Choice: The choice object corresponding to the specified identifier.
    
    Raises:
      ValueError: If no choice is found with the specified identifier.
    """
    choice = self.repository.get_choice_by_id(choice_id)
    if not choice:
      raise ValueError(f"Choice with id {choice_id} not found.")
    return choice
  
  def update_choice(self, choice_id: str, choice_data: dict) -> Choice:
    """
    Update an existing choice.

    Args:
      choice_id (str): The identifier of the choice to update.
      choice_data (dict): The new data of the choice as a dictionary.

    Returns:
      Choice: The updated Choice object.
    
    Raises:
      ValueError: If no choice is found with the specified identifier.
    """
    existing_choice = self.repository.get_choice_by_id(choice_id)
    if not existing_choice:
      raise ValueError(f"Choice with id {choice_id} not found.")
    
    existing_choice.page_id = choice_data.get('pageId', existing_choice.page_id)
    existing_choice.send_to_page_id = choice_data.get('sendToPageId', existing_choice.send_to_page_id)
    existing_choice.title = choice_data.get('title', existing_choice.title)

    return self.repository.update_choice(existing_choice)
  
  def delete_choice(self, choice_id:str) -> bool:
    """
    Delete a choice by its identifier.

    Args:
      choice_id (str): The identifier of the choice to delete.

    Returns:
      bool: True if the choice is successfully deleted, False otherwise.
    
    Raises:
      ValueError: If no choice is found with the specified identifier.
    """
    existing_choice = self.repository.get_choice_by_id(choice_id)
    if not existing_choice:
        raise ValueError(f"Choice with id {choice_id} not found.")
    return self.repository.delete_choice(choice_id)
  
  
