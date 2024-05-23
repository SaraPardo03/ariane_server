from marshmallow import Schema, fields

class update_user(Schema):
  firstName = fields.String()
  lastName = fields.String()
  userName = fields.String()
  email = fields.String()
  password = fields.String()