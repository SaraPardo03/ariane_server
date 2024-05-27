from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint

from utils.jwt_decorator import jwt_required

from .choices_service import choices_service

from .dto.request.choice_create import create_choice
from .dto.request.choice_update import update_choice
from .dto.response.choice_response import choice_response, choices_response

from .choice_mapper import to_dict, to_entity

choices_service = choices_service()

choices = Blueprint("choices", "choices", url_prefix="/choices", description="choices routes")

@choices.route("/<page_id>")
class choice_controller(MethodView):
  """
    Controller class for managing choices.

    This controller provides endpoints for retrieving, creating, updating, and deleting choices.
  """
  @choices.response(200, choices_response)
  @jwt_required
  def get(self, page_id:str):
    """
      Retrieve all choices associated with a page_id.

      Args:
          page_id (str): The identifier of the page whose choices are to be retrieved.

      Returns:
          dict: A dictionary containing the list of choices associated with the specified page_id.
      
      Raises:
          Exception: If an error occurs while retrieving the choices.
    """
    try:
      choices = choices_service.get_all(page_id)
      
      choices = [to_dict(choice) for choice in choices]
      return {"choices": choices}
    except Exception as e:
      return jsonify({"error": str(e)}), 500
  
  @choices.response(status_code=200)
  @jwt_required
  def delete(self, page_id:str):
    """
      Delete all choices associated with a page_id.

      Args:
          page_id (str): The identifier of the page whose choices are to be deleted.

      Returns:
          int: the number of choices deleted
      
      Raises:
          Exception: If an error occurs while deleting the choices.
    """
    try:
      count_choices_deleted = choices_service.delete_all(page_id)
      return {"pages": count_choices_deleted}
    except Exception as e:
      return jsonify({"error": str(e)}), 500
        
  @choices.arguments(create_choice)
  @choices.response(201, choice_response)
  @jwt_required
  def post(self, choice_data:dict, page_id:str):
    """
      Create a new choice for a page.

      Args:
          choice_data (dict): The data for the new choice.
          page_id (str): The identifier of the page for whom the choice is created.

      Returns:
          dict: A dictionary containing the created choice.
      
      Raises:
          ValueError: If the provided data is invalid.
          Exception: If an error occurs while creating the choice.
    """
    try:
      choice = choices_service.create_choice(to_entity(choice_data))
    except ValueError as ve:
      return jsonify({"error": str(ve)}), 400
    except Exception as e:
      return jsonify({"error": str(e)}), 500
  
    return jsonify({"choice": to_dict(choice)})

  @choices.route("/choice/<choice_id>")
  class choice_controller(MethodView):
    """
      Controller class for managing individual choice.
    """
    @choices.response(200, choice_response)
    @jwt_required
    def get(self, choice_id:str):
      """
        Retrieve a choice by its identifier.

        Args:
            choice_id (str): The identifier of the choice to retrieve.
        Returns:
            dict: A dictionary containing the retrieved choice.
        
        Raises:
            ValueError: If no choice is found with the specified identifier.
            Exception: If an error occurs while retrieving the choice.
      """
      try:
          choice = choices_service.get_choice_by_id(choice_id)
          return jsonify({"choice": to_dict(choice)})
      except ValueError as ve:
          return jsonify({"error": str(ve)}), 404
      except Exception as e:
          return jsonify({"error": str(e)}), 500
      
    @choices.arguments(update_choice)
    @choices.response(200, choice_response)
    @jwt_required
    def put(self, choice_data:dict, choice_id:str):
      """
        Update a choice by its identifier.

        Args:
            choice_data (dict): The updated data for the choice.
            choice_id (str): The identifier of the choice to update.

        Returns:
            dict: A dictionary containing the updated choice.
        
        Raises:
            ValueError: If no choice is found with the specified identifier or the provided data is invalid.
            Exception: If an error occurs while updating the choice.
        """
      try:
        updated_choice = choices_service.update_choice(choice_id, choice_data)
        return jsonify({"choice": to_dict(updated_choice)})
      except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
      except Exception as e:
        return jsonify({"error": str(e)}), 500
      
    @choices.response(status_code=200)
    @jwt_required
    def delete(self, choice_id:str):
      """
        Delete a choice by its identifier.

        Args:
            choice_id (str): The identifier of the choice to delete.
        Returns:
            dict: A dictionary containing a success message if the choice is deleted successfully.
        
        Raises:
            ValueError: If no choice is found with the specified identifier.
            Exception: If an error occurs while deleting the choice.
        """
      try:
        success = choices_service.delete_choice(choice_id)
        if not success:
            return jsonify({"error": "Choice not found"}), 404
        return jsonify({"message": "Choice successfully deleted"}), 200
      except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
      except Exception as e:
        return jsonify({"error": str(e)}), 500
      
choice_send_to = Blueprint("choice_send_to", "choice_send_to", url_prefix="/choice_send_to", description="choice_send_to routes")

@choice_send_to.route("/<send_to_page_id>")
class choice_send_to_controller(MethodView):
  """
    Controller class for managing choices.

    This controller provides endpoints for retrieving choice
  """
  @choices.response(200, choice_response)
  @jwt_required
  def get(self, send_to_page_id:str):
    """
    Retrieve a choice by its identifier of the page to by send to.

    Args:
        send_to_page_id_id (str): The identifier of the page to by send.

    Returns:
          dict: A dictionary containing the retrieved choice.

    Raises:
        ValueError: If no choice is found with the specified identifier.
        Exception: If an error occurs while retrieving the choice.
    """
    try:
        choice = choices_service.get_choice_by_send_to_page_id(send_to_page_id)
        print("controller", choice)
        return jsonify({"choice": to_dict(choice)})
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
  