from flask_restplus import Resource
from api import api, directory_creator

ns = api.namespace('resources/issues', description='Operations related to issues located in management module')

@ns.route('/<int:kanban_id>')
class IssuesAll(Resource):
    @api.response(200, "Issues for kanban board fetched")
    def get(self, kanban_id):
        return {"response": "OK", "kanban_id": kanban_id}, 200