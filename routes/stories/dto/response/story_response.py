from marshmallow import Schema, fields

from routes.pages.dto.response.page_response import page_response
# Define a schema for the reponse
class story_response(Schema):
  id = fields.String(required=True)
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
  pages = fields.List(fields.Nested(page_response), allow_none=True)

class stories_response(Schema):
  stories = fields.List(fields.Nested(story_response))