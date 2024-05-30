from marshmallow import Schema, fields

# Define a schema for creating a story 
class update_story(Schema):
  title = fields.String()
  summary = fields.String()
  cover = fields.String(allow_none=True)
  updatedAt = fields.String()
  totalCharacters = fields.Integer()
  totalEnd = fields.Integer()
  totalPages = fields.Integer()
  totalOpenNode = fields.Integer()
