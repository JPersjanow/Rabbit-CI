from flask import Flask, Blueprint
from tools.log import setup_custom_logger
from api import api
from kanbans_namespace import ns as kanban_namespace

app = Flask(__name__)
logger = setup_custom_logger('api_server')

def initialize_app(flask_app):
    logger.info("Initializing api server")
    blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
    api.init_app(blueprint)
    api.add_namespace(kanban_namespace)
    flask_app.register_blueprint(blueprint)

def main():
    logger.info("Starting api server")
    initialize_app(app)
    app.run(debug='DEBUG')

if __name__ == '__main__':
    main()
