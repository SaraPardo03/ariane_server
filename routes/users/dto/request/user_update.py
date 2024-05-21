from marshmallow import Schema, fields

class update_user(Schema):
  firstname = fields.String()
  lastname = fields.String()
  username = fields.String()
  email = fields.String()
  password = fields.String()