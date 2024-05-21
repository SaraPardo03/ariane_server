from marshmallow import Schema, fields

class create_user(Schema):
  firstname = fields.String()
  lastname = fields.String()
  username = fields.String()
  email = fields.String(required=True)
  password = fields.String(required=True)