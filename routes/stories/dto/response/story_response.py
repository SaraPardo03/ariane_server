from marshmallow import Schema, fields

# Define a schema for the reponse
class story_response(Schema):
  user_id= fields.String(required=True)
  title = fields.String(required=True) 
  summary = fields.String()

class story_full_response(story_response):
  _id = fields.String(required=True)

class stories_response(Schema):
  stories = fields.List(fields.Nested(story_response))