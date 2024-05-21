from marshmallow import Schema, fields

# Define a schema for the reponse
class user_response(Schema):
  firstname = fields.String() 
  lastname = fields.String()
  username = fields.String()
  email = fields.String(required=True)
  password = fields.String(required=True)
  salt = fields.String(required=True)
  

class user_full_response(user_response):
  _id = fields.String(required=True)
  

class users_response(Schema):
  users = fields.List(fields.Nested(user_response))