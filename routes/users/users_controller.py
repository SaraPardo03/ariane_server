from flask.views import MethodView
from flask import request, jsonify
from flask_smorest import Blueprint

from utils.jwt_helpers import generate_token

from .user import User
from .users_service import users_service

from .dto.response.user_response import user_response, user_full_response, users_response
from .dto.request.user_auth import auth_user
from .dto.request.user_create import create_user
from .dto.request.user_update import update_user

from .user_mapper import to_dict, to_entity

users_service = users_service()

sign_up = Blueprint("sign_up", "sign_up", url_prefix="/sign_up", description="sign up routes")
 
@sign_up.route("/")
class sign_up_controller(MethodView):
  @sign_up.arguments(create_user)
  @sign_up.response(201, user_response)
  def post(self, user_data:dict):
    email = user_data.get("email")
    password = user_data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400
    try:
      user = users_service.create_user(to_entity(user_data))
    except ValueError as ve:
          return jsonify({"error": str(ve)}), 409
    if user:
        token = generate_token(user.id)
        return jsonify(access_token=token), 201
    else:
        return jsonify({"message": "User creation failed"}), 500

sign_in = Blueprint("sign_in", "sign_in", url_prefix="/sign_in", description="sign in routes")

@sign_in.route('/')
class sign_in_controller(MethodView):
  @sign_in.arguments(auth_user)
  @sign_in.response(200, user_response)
  def post(self, user_data:dict):
    email = user_data.get("email")
    password = user_data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = users_service.get_user_by_email(email)

    if not user:
      return jsonify({"message": "User not found"}), 404
  
    if not users_service.check_password(user, password):
        return jsonify({"message": "Incorrect password"}), 401
    
    token = generate_token(str(user.id))
    return jsonify(access_token=token), 200

    
users = Blueprint("users", "users", url_prefix="/users", description="users routes")
 
@users.route("/")
class users_controller(MethodView):
  @users.response(200, users_response)
  def get(self):
    try:
      users = users_service.get_all()
      return {"users": users}
    except Exception as e:
      return jsonify({"error": str(e)}), 500
  
  @users.arguments(create_user)
  @users.response(201, user_full_response)
  def post(self, user_data: dict):
    return users_service.create_user(to_entity(user_data))
   
  @users.route("/<user_id>")
  class user_controller(MethodView):
    @users.response(200, user_response)
    def get(self, user_id:str,):
      try:
          user = users_service.get_user_by_id(user_id)
          return to_dict(user)
      except ValueError as ve:
          return jsonify({"error": str(ve)}), 404
      except Exception as e:
          return jsonify({"error": str(e)}), 500
          
    @users.response(200)
    def delete(self, user_id:str,):
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
      try:
        updated_user = users_service.update_user(user_id, user_data)
        return to_dict(updated_user)
      except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
      except Exception as e:
        return jsonify({"error": str(e)}), 500