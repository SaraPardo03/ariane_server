from marshmallow import Schema, fields

class auth_user(Schema):
  email = fields.String(required=True)
  password = fields.String(required=True)