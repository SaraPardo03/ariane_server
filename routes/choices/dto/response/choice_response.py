from marshmallow import Schema, fields

# Define a schema for the reponse
class choice_response(Schema):
  id = fields.String(required=True)
  pageId = fields.String(required=True)
  sendToPageId = fields.String(required=True)
  title = fields.String(required=True)



class choices_response(Schema):
  choices = fields.List(fields.Nested(choice_response))