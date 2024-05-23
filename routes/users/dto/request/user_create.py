from marshmallow import Schema, fields

class create_user(Schema):
  firstName = fields.String()
  lastName = fields.String()
  userName = fields.String()
  email = fields.String(required=True)
  password = fields.String(required=True)