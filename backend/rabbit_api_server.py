from flask import Flask, Blueprint
from flask_cors import CORS
from tools.log import setup_custom_logger
from api import api, logger
from kanbans_namespace import ns as kanban_namespace
from issues_namespace import ns as issues_namespace

app = Flask(__name__)
CORS(app=app)


def initialize_app(flask_app):
    logger.info("Configuring api server")
    blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
    api.init_app(blueprint)
    api.add_namespace(kanban_namespace)
    api.add_namespace(issues_namespace)
    flask_app.register_blueprint(blueprint)


def main():
    logger.info("Starting api server")
    initialize_app(app)
    app.run(debug="DEBUG")


if __name__ == "__main__":
    main()
