from marshmallow import Schema, fields

# Define a schema for creating a page 
class create_page(Schema):
  storyId = fields.String(required=True)
  previousPageId = fields.String(allow_none=True)
  title = fields.String(required=True)
  text = fields.String()
  end = fields.Boolean()
  first = fields.Boolean()
  totalCharacters = fields.Integer()
  image = fields.String(required=True)

