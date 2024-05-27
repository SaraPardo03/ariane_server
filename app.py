from flask import Flask
from flask_smorest import Api

from flask_cors import CORS

from routes.users.users_controller import users, sign_in, sign_up
from routes.stories.stories_controller import stories
from routes.pages.pages_controller import pages
from routes.choices.choices_controller import choices, choice_send_to


server = Flask(__name__)
#CORS(server, resources={r"/*": {"origins": "http://localhost:5173"}})
# Configuration de CORS pour plusieurs origines
cors = CORS(server, resources={
    r"/*": {
        "origins": ["http://localhost:5173", "http://192.168.1.109:5173"]
    }
})

class APIConfig:
  API_TITLE = "Ariane Library API V1"
  API_VERSION = "v1"
  OPENAPI_VERSION = "3.0.2"
  OPENAPI_URL_PREFIX = "/"
  OPENAPI_SWAGGER_UI_PATH = "/docs"
  OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
  OPENAPI_REDOC_PATH = "/redoc"
  OPENAPI_REDOC_UI_URL = "https://cdn.jsdelivr.net/npm/redoc@latest/bundles/redoc.standalone.js"

server.config.from_object(APIConfig)

api = Api(server)

api.register_blueprint(users)
api.register_blueprint(sign_in)
api.register_blueprint(sign_up)
api.register_blueprint(stories)
api.register_blueprint(pages)
api.register_blueprint(choices)
api.register_blueprint(choice_send_to)

@server.route("/")
def index():
  return {"message": "Hello, Ariane!"}

if __name__ == "__main__":
  server.run(debug=True, port=8080, host="0.0.0.0")

