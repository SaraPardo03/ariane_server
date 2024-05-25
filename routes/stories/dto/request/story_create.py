from marshmallow import Schema, fields

# Define a schema for creating a story 
class create_story(Schema):
  userId = fields.String(required=True)
  title = fields.String(required=True)
  summary = fields.String()
  createdAt = fields.String()
  updatedAt = fields.String()
  totalCharacters = fields.Integer()
  totalEnd = fields.Integer()
  totalPages = fields.Integer()
  totalOpenNode = fields.Integer()
