from marshmallow import Schema, fields

# Define a schema for the reponse
class user_response(Schema):
  id = fields.String(required=True)
  email = fields.String(required=True)
  password = fields.String(required=True)
  salt = fields.String(required=True)
  firstName = fields.String() 
  lastName = fields.String()
  userName = fields.String()
  token = fields.String()
  

class users_response(Schema):
  users = fields.List(fields.Nested(user_response))