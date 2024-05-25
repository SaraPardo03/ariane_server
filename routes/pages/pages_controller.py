from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint

from utils.jwt_decorator import jwt_required

from .pages_service import pages_service

from .dto.request.page_create import create_page
from .dto.request.page_update import update_page
from .dto.response.page_response import page_response, pages_response

from .page_mapper import to_dict, to_entity

pages_service = pages_service()

pages = Blueprint("pages", "pages", url_prefix="/pages", description="pages routes")

@pages.route("/<story_id>")
class pages_controller(MethodView):
  """
    Controller class for managing pages.

    This controller provides endpoints for retrieving, creating, updating, and deleting pages.
  """
  @pages.response(200, pages_response)
  @jwt_required
  def get(self, story_id:str):
    """
      Retrieve all pages associated with a story_id.

      Args:
          story_id (str): The identifier of the story whose pages are to be retrieved.

      Returns:
          dict: A dictionary containing the list of pages associated with the specified story_id.
      
      Raises:
          Exception: If an error occurs while retrieving the pages.
    """
    try:
      pages = pages_service.get_all(story_id)
      pages = [to_dict(page) for page in pages]
      return {"pages": pages}
    except Exception as e:
      return jsonify({"error": str(e)}), 500
  
  @pages.response(status_code=200)
  @jwt_required
  def delete(self, story_id:str):
    """
      Delete all pages associated with a story_id.

      Args:
          story_id (str): The identifier of the story whose pages are to be deleted.

      Returns:
          int: the number of pages deleted
      
      Raises:
          Exception: If an error occurs while deleting the pages.
    """
    try:
      count_pages_deleted = pages_service.delete_all(story_id)
      return {"pages": count_pages_deleted}
    except Exception as e:
      return jsonify({"error": str(e)}), 500
        
  @pages.arguments(create_page)
  @pages.response(201, page_response)
  @jwt_required
  def post(self, page_data:dict, story_id:str):
    """
      Create a new page for a story.

      Args:
          page_data (dict): The data for the new page.
          story_id (str): The identifier of the story for whom the page is created.

      Returns:
          dict: A dictionary containing the created page.
      
      Raises:
          ValueError: If the provided data is invalid.
          Exception: If an error occurs while creating the page.
    """
    try:
      page = pages_service.create_page(to_entity(page_data))
    except ValueError as ve:
      return jsonify({"error": str(ve)}), 400
    except Exception as e:
      return jsonify({"error": str(e)}), 500
  
    return jsonify({"page": to_dict(page)})

  @pages.route("/page/<page_id>")
  class page_controller(MethodView):
    """
      Controller class for managing individual page.
    """
    @pages.response(200, page_response)
    @jwt_required
    def get(self, page_id:str):
      """
        Retrieve a page by its identifier.

        Args:
            page_id (str): The identifier of the page to retrieve.
        Returns:
            dict: A dictionary containing the retrieved page.
        
        Raises:
            ValueError: If no page is found with the specified identifier.
            Exception: If an error occurs while retrieving the page.
      """
      try:
          page = pages_service.get_page_by_id(page_id)
          return jsonify({"page": to_dict(page)})
      except ValueError as ve:
          return jsonify({"error": str(ve)}), 404
      except Exception as e:
          return jsonify({"error": str(e)}), 500
      
    @pages.arguments(update_page)
    @pages.response(200, page_response)
    @jwt_required
    def put(self, page_data:dict, page_id:str):
      """
        Update a page by its identifier.

        Args:
            page_data (dict): The updated data for the page.
            page_id (str): The identifier of the page to update.

        Returns:
            dict: A dictionary containing the updated page.
        
        Raises:
            ValueError: If no page is found with the specified identifier or the provided data is invalid.
            Exception: If an error occurs while updating the page.
        """
      try:
        updated_page = pages_service.update_page(page_id, page_data)
        return jsonify({"page": to_dict(updated_page)})
      except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
      except Exception as e:
        return jsonify({"error": str(e)}), 500
      
    @pages.response(status_code=200)
    @jwt_required
    def delete(self, page_id:str):
      """
        Delete a page by its identifier.

        Args:
            page_id (str): The identifier of the page to delete.
        Returns:
            dict: A dictionary containing a success message if the page is deleted successfully.
        
        Raises:
            ValueError: If no page is found with the specified identifier.
            Exception: If an error occurs while deleting the page.
        """
      try:
        success = pages_service.delete_page(page_id)
        if not success:
            return jsonify({"error": "Page not found"}), 404
        return jsonify({"message": "Page successfully deleted"}), 200
      except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
      except Exception as e:
        return jsonify({"error": str(e)}), 500