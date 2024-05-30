from marshmallow import Schema, fields

# Define a schema for creating a story 
class create_story(Schema):
  userId = fields.String(required=True)
  title = fields.String(required=True)
  summary = fields.String()
  cover = fields.String(allow_none=True)
  createdAt = fields.String()
  updatedAt = fields.String()
  totalCharacters = fields.Integer()
  totalEnd = fields.Integer()
  totalPages = fields.Integer()
  totalOpenNode = fields.Integer()
