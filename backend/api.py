from flask_restplus import Api
from directory_creator import DirectoryCreator

api = Api(version='0.2', title='Rabbit-CI API',description='This is a REST API for Rabbit-CI')
directory_creator = DirectoryCreator()

