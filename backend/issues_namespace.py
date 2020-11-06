from flask_restplus import Resource, fields
from flask import jsonify
from api import api

from tools.issues_tools import IssueCreator, IssueFinder
from tools.config_reader import ConfigReader

ns = api.namespace('resources/issues', description='Operations related to issues located in management module')
issue_model = api.model('Issue Model', {
    'name': fields.String(required=True, description='Issue name'),
    'description': fields.String(required=False, description='Issue description'),
    'creator': fields.String(required=False, description='User-creator of the issue')
})

config = ConfigReader()

@ns.route('/<int:kanban_id>')
class IssuesAll(Resource):
    @api.response(200, "Issues for kanban board fetched")
    @api.response(404, "Unable to fetch issues")
    def get(self, kanban_id):
        """ Return all issues info for given kanban board """
        issue_finder = IssueFinder()
        try:
            all_issues_info_list = issue_finder.return_all_issues_info_for_kanban(kanbans_directory=config.kanbans_directory, kanban_id=kanban_id)
            response = jsonify(all_issues_info_list)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        except Exception as e:
            return {"response": "Couldn't fetch issues", "exception": str(e)}, 500
        finally:
            del(issue_finder)

    @ns.expect(issue_model)
    @api.response(201, "Issue has been created")
    @api.response(500, "Unable to create issue")
    def post(self, kanban_id):
        """ Create new issue for given kanban board """
        issue_creator = IssueCreator()
        issue_xml_tree = issue_creator.create_xml_tree_for_issue_config(issue_name=api.payload['name'], kanban_id=kanban_id, issue_description=api.payload['description'])
        try:
            issues_directory = issue_creator.create_issues_folder(kanbans_directory=config.kanbans_directory, kanban_id=kanban_id)
        except Exception as e:
            del(issue_creator)
            return {"response": "Unable to create issues directory!", "exception": str(e)}, 500
        try:
            issue_creator.create_new_issue_config(kanbans_directory=config.kanbans_directory, kanban_id=kanban_id, issues_directory=issues_directory, issue_name=api.payload['name'], xml_tree=issue_xml_tree)
            return {"response": f"Issue with name {api.payload['name']} for kanban with id {kanban_id} created!"}, 201
        except Exception as e:
            del(issue_creator)
            return {"response": "Unable to create new issue!", "exception": str(e)}, 500

        

@ns.route('/<int:kanban_id>/<string:issue_name>')
class IssueSingle(Resource):
    def get(self, kanban_id, issue_name):
        """ Return specific issue info with given name for given kanban board """
        return {"response": "OK"}, 200

    @ns.expect(issue_model)
    def put(self, kanban_id, issue_name):
        return {"response": "OK"}, 200
    