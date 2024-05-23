from marshmallow import Schema, fields

# Define a schema for creating a page 
class update_story(Schema):
  title = fields.String()
  summary = fields.String()
  updatedAt = fields.String()
  totalCharacters = fields.Integer()
  totalEnd = fields.Integer()
  totalPages = fields.Integer()
  totalOpenNode = fields.Integer()
