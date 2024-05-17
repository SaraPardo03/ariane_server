from flask.views import MethodView
from flask_smorest import Blueprint

from .story import Story
from .stories_service import stories_service

from .dto.request.story_create import create_story
from .dto.response.story_response import story_response, story_full_response, stories_response

from .story_mapper import to_entity, to_dict

stories_service = stories_service()

stories = Blueprint("stories", "stories", url_prefix="/stories", description="stories routes")
 
@stories.route("/")
class stories_controller(MethodView):
  @stories.response(status_code=200, schema=stories_response)
  def get(self):
    return {"stories": stories_service.get_all()}
  
  @stories.arguments(create_story)
  @stories.response(status_code=201, schema=story_full_response)
  def post(self, story: dict):
    new_story = Story(user_id=story['user_id'], title=story['title'], summary=story['summary'])
    created_story = stories_service.create_story(new_story)
    return to_dict(created_story)