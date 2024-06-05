from marshmallow import Schema, fields

# Define a schema for creating a page 
class update_page(Schema):
  title = fields.String()
  text = fields.String()
  end = fields.Boolean()
  first = fields.Boolean()
  totalCharacters = fields.Integer()
  image = fields.String(allow_none=True)
