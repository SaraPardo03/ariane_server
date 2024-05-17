from marshmallow import Schema, fields

# Define a schema for creating a page 
class update_story(Schema):
  user_id = fields.String(required=True)
  title = fields.String(required=True)
  summary = fields.String()
