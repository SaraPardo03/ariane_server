from marshmallow import Schema, fields

# Define a schema for the reponse
class page_response(Schema):
  title = fields.String()  # Title of the page as a string
  text = fields.String()  # Text content of the page as a string
  first = fields.Boolean()  # Boolean flag indicating if this is the first page
  end = fields.Boolean()  # Boolean flag indicating if this is an end page
  totalCharacters = fields.Integer()  # Total number of characters in the page (text only)

class page_full_response(page_response):
  id = fields.String()