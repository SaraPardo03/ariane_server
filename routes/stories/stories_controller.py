import jwt

from flask.views import MethodView
from flask import abort
from flask import jsonify
from flask_smorest import Blueprint

from .story import Story
from .stories_service import stories_service

from .dto.request.story_create import create_story
from .dto.request.story_update import update_story
from .dto.response.story_response import story_response, story_full_response, stories_response

from .story_mapper import to_entity, to_dict

stories_service = stories_service()

stories = Blueprint("stories", "stories", url_prefix="/stories", description="stories routes")
 
@stories.route("/<user_id>")
class stories_controller(MethodView):
  """
    Controller class for managing stories.

    This controller provides endpoints for retrieving, creating, updating, and deleting stories.
  """
  @stories.response(status_code=200, schema=stories_response)
  def get(self, user_id:str):
    """
      Retrieve all stories associated with a user.

      Args:
          user_id (str): The identifier of the user whose stories are to be retrieved.

      Returns:
          dict: A dictionary containing the list of stories associated with the specified user.
      
      Raises:
          Exception: If an error occurs while retrieving the stories.
    """
    try:
      stories = stories_service.get_all(user_id)
      return {"stories": stories}
    except Exception as e:
      return jsonify({"error": str(e)}), 500
      
  @stories.arguments(create_story)
  @stories.response(status_code=201, schema=story_full_response)
  def post(self, story_data:dict, user_id:str):
    """
      Create a new story for a user.

      Args:
          story_data (dict): The data for the new story.
          user_id (str): The identifier of the user for whom the story is created.

      Returns:
          dict: A dictionary containing the created story.
      
      Raises:
          ValueError: If the provided data is invalid.
          Exception: If an error occurs while creating the story.
    """
    try:
      new_story = Story(user_id=user_id, title=story_data['title'], summary=story_data['summary'])
      created_story = stories_service.create_story(new_story)
      return to_dict(created_story)
    
    except ValueError as ve:
      return jsonify({"error": str(ve)}), 400
      #abort(400, description=str(ve))
    except Exception as e:
      return jsonify({"error": str(e)}), 500
  


  @stories.route("/<user_id>/<story_id>")
  class story_controller(MethodView):
    """
      Controller class for managing individual stories.
    """
    @stories.response(status_code=200, schema=story_response)
    def get(self, story_id:str, user_id:str,):
      """
        Retrieve a story by its identifier.

        Args:
            story_id (str): The identifier of the story to retrieve.
            user_id (str): The identifier of the user who owns the story.

        Returns:
            dict: A dictionary containing the retrieved story.
        
        Raises:
            ValueError: If no story is found with the specified identifier.
            Exception: If an error occurs while retrieving the story.
      """
      try:
          story = stories_service.get_story_by_id(story_id)
          return to_dict(story)
      except ValueError as ve:
          return jsonify({"error": str(ve)}), 404
      except Exception as e:
          return jsonify({"error": str(e)}), 500
          
    @stories.response(status_code=200)
    def delete(self, story_id:str, user_id:str,):
      """
        Delete a story by its identifier.

        Args:
            story_id (str): The identifier of the story to delete.
            user_id (str): The identifier of the user who owns the story.

        Returns:
            dict: A dictionary containing a success message if the story is deleted successfully.
        
        Raises:
            ValueError: If no story is found with the specified identifier.
            Exception: If an error occurs while deleting the story.
        """
      try:
        success = stories_service.delete_story(story_id)
        if not success:
            return jsonify({"error": "Story not found"}), 404
        return jsonify({"message": "Story successfully deleted"}), 200
      except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
      except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    @stories.arguments(update_story)
    @stories.response(status_code=200, schema=story_response)
    def put(self, story_data:dict, story_id:str, user_id:str,):
      """
        Update a story by its identifier.

        Args:
            story_data (dict): The updated data for the story.
            story_id (str): The identifier of the story to update.
            user_id (str): The identifier of the user who owns the story.

        Returns:
            dict: A dictionary containing the updated story.
        
        Raises:
            ValueError: If no story is found with the specified identifier or the provided data is invalid.
            Exception: If an error occurs while updating the story.
        """
      try:
        updated_story = stories_service.update_story(story_id, story_data)
        return to_dict(updated_story)
      except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
      except Exception as e:
        return jsonify({"error": str(e)}), 500