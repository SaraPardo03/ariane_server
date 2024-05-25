from .pages_repository import pages_repository
from .page import Page

class pages_service:
  """
  Service for managing pages.

  This service acts as an interface between the API routes and the data repository
  to perform operations related to pages.
  """
  def __init__(self):
    """
    Initialize a new pages_service object.

    This constructor creates an instance of pages_repository to interact
    with the database.
    """
    self.repository = pages_repository()
  
  def get_all(self, story_id:str) -> list[dict]:
    """
    Retrieve all pages associated with a story_id.

    Args:
      story_id (str): The story identifier.

    Returns:
      list[dict]: A list containing the information of all the story pages.
    
    Raises:
      Exception: If an error occurs while fetching the pages.
    """
    try:
      return self.repository.get_all(story_id)
    except Exception as e:
      raise Exception(f"Failed to fetch pages: {e}") from e
    
  def delete_all(self, story_id:str) -> int:
    """
    Delete all pages associated with a story_id.

    Args:
      story_id (str): The story identifier.

    Returns:
      int: the number of pages deleted
    
    Raises:
      Exception: If an error occurs while deleting the pages.
    """
    try:
      return self.repository.delete_all(story_id)
    except Exception as e:
      raise Exception(f"Failed to delete pages: {e}") from e
  
  def create_page(self, p: Page) -> Page:
    """
    Create a new page.

    Args:
      p (Page): The Page object containing the information of the new page.

    Returns:
      Page: The created Page object.

    Raises:
      ValueError: If any of the required values to create the page is missing.
      Exception: If an error occurs while creating the pages.
    """
    try:
      return self.repository.create_page(p)
    except ValueError as ve:
      raise ValueError(f"Missing required values to create the page: {ve}") from ve
    except Exception as e:
      raise Exception(f"Failed to create page: {e}") from e
    
  
  def get_page_by_id(self, page_id:str) -> Page:
    """
    Retrieve a page by its identifier.

    Args:
      page_id (str): The identifier of the page.

    Returns:
      Page: The Page object corresponding to the specified identifier.
    
    Raises:
      ValueError: If no page is found with the specified identifier.
    """
    page = self.repository.get_page_by_id(page_id)
    if not page:
      raise ValueError(f"Page with id {page_id} not found.")
    return page
  
  def update_page(self, page_id: str, page_data: dict) -> Page:
    """
    Update an existing page.

    Args:
      page_id (str): The identifier of the page to update.
      page_data (dict): The new data of the page as a dictionary.

    Returns:
      Page: The updated Page object.
    
    Raises:
      ValueError: If no page is found with the specified identifier.
    """
    existing_page = self.repository.get_page_by_id(page_id)
    if not existing_page:
      raise ValueError(f"Page with id {page_id} not found.")
    
    existing_page.story_id = page_data.get('storyId', existing_page.story_id)
    existing_page.title = page_data.get('title', existing_page.title)
    existing_page.text = page_data.get('text', existing_page.text)
    existing_page.first = page_data.get('first', existing_page.first)
    existing_page.end = page_data.get('end', existing_page.end)
    existing_page.total_characters = page_data.get('totalCharacters', existing_page.total_characters)

    return self.repository.update_page(existing_page)
  
  def delete_page(self, page_id:str) -> bool:
    """
    Delete a page by its identifier.

    Args:
      page_id (str): The identifier of the page to delete.

    Returns:
      bool: True if the page is successfully deleted, False otherwise.
    
    Raises:
      ValueError: If no page is found with the specified identifier.
    """
    existing_page = self.repository.get_page_by_id(page_id)
    if not existing_page:
        raise ValueError(f"Page with id {page_id} not found.")
    return self.repository.delete_page(page_id)
  
  
