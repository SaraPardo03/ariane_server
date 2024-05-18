from marshmallow import Schema, fields

# Define a schema for creating a page 
class create_story(Schema):
  user_id = fields.String()
  title = fields.String(required=True)
  summary = fields.String()
