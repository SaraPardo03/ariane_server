from .stories_repository import stories_repository
from .story import Story

class stories_service:
  """
  Service for managing stories.

  This service acts as an interface between the API routes and the data repository
  to perform operations related to stories.
  """
  def __init__(self):
    """
    Initialize a new stories_service object.

    This constructor creates an instance of stories_repository to interact
    with the database.
    """
    self.repository = stories_repository()
  
  def get_all(self, user_id:str) -> list[dict]:
    """
    Retrieve all stories associated with a user.

    Args:
      user_id (str): The user's identifier.

    Returns:
      ist[dict]: A list containing the information of all the user's stories.
    
    Raises:
      Exception: If an error occurs while fetching the stories.
    """
    try:
      return self.repository.get_all(user_id)
    except Exception as e:
      raise Exception(f"Failed to fetch stories: {e}") from e
  
  def create_story(self, s: Story) -> Story:
    """
    Create a new story.

    Args:
      s (Story): The Story object containing the information of the new story.

    Returns:
      Story: The created Story object.

    Raises:
      ValueError: If any of the required values to create the story is missing.
    """
    return self.repository.create_story(s)
  
  def get_story_by_id(self, story_id:str) -> Story:
    """
    Retrieve a story by its identifier.

    Args:
      story_id (str): The identifier of the story.

    Returns:
      Story: The Story object corresponding to the specified identifier.
    
    Raises:
      ValueError: If no story is found with the specified identifier.
    """
    story = self.repository.get_story_by_id(story_id)
    if not story:
      raise ValueError(f"Story with id {story_id} not found.")
    return story
  
  def update_story(self, story_id: str, story_data: dict) -> Story:
    """
    Update an existing story.

    Args:
      story_id (str): The identifier of the story to update.
      story_data (dict): The new data of the story as a dictionary.

    Returns:
      Story: The updated Story object.
    
    Raises:
      ValueError: If no story is found with the specified identifier.
    """
    existing_story = self.repository.get_story_by_id(story_id)
    if not existing_story:
      raise ValueError(f"Story with id {story_id} not found.")
    
    existing_story.user_id = story_data.get('userId', existing_story.user_id)
    existing_story.title = story_data.get('title', existing_story.title)
    existing_story.summary = story_data.get('summary', existing_story.summary)
    existing_story.cover = story_data.get('cover', existing_story.cover)
    existing_story.created_at = story_data.get('createdAt', existing_story.created_at)
    existing_story.updated_at = story_data.get('updatedAt', existing_story.updated_at)
    existing_story.total_characters = story_data.get('totalCharacters', existing_story.total_characters)
    existing_story.total_end = story_data.get('totalEnd', existing_story.total_end)
    existing_story.total_pages = story_data.get('totalPages', existing_story.total_pages)
    existing_story.total_open_node = story_data.get('totalOpenNode', existing_story.total_open_node)

    return self.repository.update_story(existing_story)
  
  def delete_story(self, story_id:str) -> bool:
    """
    Delete a story by its identifier.

    Args:
      story_id (str): The identifier of the story to delete.

    Returns:
      bool: True if the story is successfully deleted, False otherwise.
    
    Raises:
      ValueError: If no story is found with the specified identifier.
    """
    existing_story = self.repository.get_story_by_id(story_id)
    if not existing_story:
        raise ValueError(f"Story with id {story_id} not found.")
    return self.repository.delete_story(story_id)
  
  
