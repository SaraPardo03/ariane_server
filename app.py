from flask import Flask
from flask_smorest import Api

from routes.pages.pages_controller import pages

server = Flask(__name__)

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

api.register_blueprint(pages)

@server.route("/")
def index():
  return {"message": "Hello, Ariane!"}

if __name__ == "__main__":
  server.run(debug=True, port=8080, host="0.0.0.0")
