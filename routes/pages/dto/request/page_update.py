from  marshmallow import Schema, fields

# Define a schema for updating a page 
class update_page(Schema):
  title = fields.String()  # Title of the page as a string
  text = fields.String()  # Text content of the page as a string
  first = fields.Boolean()  # Boolean flag indicating if this is the first page
  end = fields.Boolean()  # Boolean flag indicating if this is an end page
  totalCharacters = fields.Integer()  # Total number of characters in the page (text only)