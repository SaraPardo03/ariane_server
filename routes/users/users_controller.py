from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint

from utils.jwt_helpers import generate_token

from .users_service import users_service

from .dto.response.user_response import user_response, users_response
from .dto.request.user_auth import auth_user
from .dto.request.user_create import create_user
from .dto.request.user_update import update_user

from .user_mapper import to_dict, to_entity 

# Initialize the users_service instance
users_service = users_service()

# Define the blueprint for sign-up routes
sign_up = Blueprint("sign_up", "sign_up", url_prefix="/sign_up", description="sign up routes")
 
@sign_up.route("/")
class sign_up_controller(MethodView):
  @sign_up.arguments(create_user)
  @sign_up.response(201, user_response)
  def post(self, user_data:dict):
    """
      Handle user sign-up.

      Expects user data in JSON format with 'email' and 'password' fields.

      Returns:
        - 201: User successfully created with a JWT token.
        - 400: Missing email or password.
        - 409: User creation conflict (e.g., email already exists).
        - 500: Internal server error.
    """
    email = user_data.get("email")
    password = user_data.get("password")

    if not email or not password:
      return jsonify({"message": "Email and password are required"}), 400
    try:
      user = users_service.create_user(to_entity(user_data))
    except ValueError as ve:
      return jsonify({"error": str(ve)}), 409
    except Exception as e:
      return jsonify({"error": str(e)}), 500
    
    if user:
      token = generate_token(user.id)
      user.token = token
      return jsonify({"user": to_dict(user)}), 201
    else:
      return jsonify({"message": "User creation failed"}), 500
  
# Define the blueprint for sign-in routes
sign_in = Blueprint("sign_in", "sign_in", url_prefix="/sign_in", description="sign in routes")

@sign_in.route('/')
class sign_in_controller(MethodView):
  @sign_in.arguments(auth_user)
  @sign_in.response(200, user_response)
  def post(self, user_data:dict):
    """
      Handle user sign-in.

      Expects user data in JSON format with 'email' and 'password' fields.

      Returns:
        - 200: User successfully authenticated with a JWT token.
        - 400: Missing email or password.
        - 401: User not found or password incorrect.
        - 500: Internal server error.
    """
    email = user_data.get("email")
    password = user_data.get("password")

    if not email or not password:
      return jsonify({"message": "Email and password are required"}), 400
    try:
      user = users_service.get_user_by_email(email)
    except Exception as e:
      return jsonify({"error": str(e)}), 500

    if not user:
      return jsonify({"message": "User credential failed"}), 401
  
    if not users_service.check_password(user, password):
      return jsonify({"message": "User credential failed"}), 401
    
    token = generate_token(str(user.id))
    user.token = token
    return jsonify({"user": to_dict(user)}), 200

# Define the blueprint for user routes  
users = Blueprint("users", "users", url_prefix="/users", description="users routes")
 
@users.route("/")
class users_controller(MethodView):
  @users.response(200, users_response)
  def get(self):
    """
      Get all users.

      Returns:
        - 200: A list of all users.
        - 500: Internal server error.
    """
    try:
      users = users_service.get_all()
      users = [to_dict(user) for user in users]
      return {"users": users}
    except Exception as e:
      return jsonify({"error": str(e)}), 500
  
  @users.arguments(create_user)
  @users.response(201, user_response)
  def post(self, user_data: dict):
    """
      Create a new user.

      Expects user data in JSON format.

      Returns:
        - 201: User successfully created.
        - 404: User creation conflict.
        - 500: Internal server error.
    """
    try:
      user = users_service.create_user(to_entity(user_data))
    except ValueError as ve:
      return jsonify({"error": str(ve)}), 404
    except Exception as e:
      return jsonify({"error": str(e)}), 500
    
    return jsonify({"user": to_dict(user)})
   
  @users.route("/<user_id>")
  class user_controller(MethodView):
    @users.response(200, user_response)
    def get(self, user_id:str,):
      """
        Get a user by ID.

        Returns:
          - 200: User found.
          - 404: User not found.
          - 500: Internal server error.
      """
      try:
        user = users_service.get_user_by_id(user_id)
        return jsonify({"user": to_dict(user)})
      except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
      except Exception as e:
        return jsonify({"error": str(e)}), 500
          
    @users.response(200)
    def delete(self, user_id:str,):
      """
        Delete a user by ID.

        Returns:
          - 200: User successfully deleted.
          - 404: User not found.
          - 500: Internal server error.
      """
      try:
        success = users_service.delete_user(user_id)
        if not success:
          return jsonify({"error": "User not found"}), 404
        return jsonify({"message": "User successfully deleted"}), 200
      except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
      except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    @users.arguments(update_user)
    @users.response(200, user_response)
    def put(self, user_data:dict, user_id:str,):
      """
        Update a user by ID.

        Expects user data in JSON format.

        Returns:
          - 200: User successfully updated.
          - 400: Invalid user data.
          - 500: Internal server error.
      """
      try:
        updated_user = users_service.update_user(user_id, user_data)
        return jsonify({"user": to_dict(updated_user)})
      except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
      except Exception as e:
        return jsonify({"error": str(e)}), 500