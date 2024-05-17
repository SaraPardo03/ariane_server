from flask.views import MethodView
from flask_smorest import Blueprint

from .pages_service import page_service

from .dto.request.page_create import create_page
from .dto.response.page_response import page_response, page_full_response

page_service = page_service()

pages = Blueprint("pages", "pages", url_prefix="/pages", description="pages routes")


@pages.route("/")
class page_controller(MethodView):
  @pages.response(status_code=200, schema=page_response(many=True))
  def get(self):
    return page_service.get_all()