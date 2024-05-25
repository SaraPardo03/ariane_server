from marshmallow import Schema, fields

# Define a schema for the reponse
class page_response(Schema):
  id = fields.String(required=True)
  storyId = fields.String(required=True)
  title = fields.String(required=True)
  text = fields.String()
  end = fields.Boolean()
  first = fields.Boolean()
  totalCharacters = fields.Integer()



class pages_response(Schema):
  pages = fields.List(fields.Nested(page_response))