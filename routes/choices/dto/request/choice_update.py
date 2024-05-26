from marshmallow import Schema, fields

# Define a schema for creating a choice 
class update_choice(Schema):
  title = fields.String()
