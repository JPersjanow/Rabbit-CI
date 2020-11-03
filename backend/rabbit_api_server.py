from flask import Flask, request, jsonify, Blueprint
from glob import glob
import os
import log
from directory_creator import DirectoryCreator
import xmltodict
from api import api, directory_creator
from kanbans_namespace import ns as kanban_namespace
app = Flask(__name__)

def initialize_app(flask_app):
    blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
    api.init_app(blueprint)
    api.add_namespace(kanban_namespace)
    flask_app.register_blueprint(blueprint)

def main():
    directory_creator.create_directory_tree()
    directory_creator.create_fake_kanbans(10)
    initialize_app(app)
    app.run(debug='DEBUG')

if __name__ == '__main__':
    main()
