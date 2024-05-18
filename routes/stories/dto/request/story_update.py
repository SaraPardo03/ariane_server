from marshmallow import Schema, fields

# Define a schema for creating a page 
class update_story(Schema):
  user_id = fields.String()
  title = fields.String()
  summary = fields.String()
