from marshmallow import Schema, fields

# Define a schema for creating a choice 
class create_choice(Schema):
  pageId = fields.String(required=True)
  sendToPageId = fields.String(required=True)
  title = fields.String(required=True)

