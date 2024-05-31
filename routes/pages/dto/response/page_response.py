import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))))

from marshmallow import Schema, fields

from routes.choices.dto.response.choice_response import choice_response
# Define a schema for the reponse
class page_response(Schema):
  id = fields.String(required=True)
  storyId = fields.String(required=True)
  title = fields.String(required=True)
  previousPageId = fields.String()
  text = fields.String()
  end = fields.Boolean()
  first = fields.Boolean()
  totalCharacters = fields.Integer()
  choices = fields.List(fields.Nested(choice_response), allow_none=True)
  choiceTitle = fields.String(allow_none=True)
  image = fields.String(allow_none=True)



class pages_response(Schema):
  pages = fields.List(fields.Nested(page_response))