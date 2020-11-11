from flask_restplus import Resource, fields
from flask import jsonify
from api import api

from tools.issues_tools import (
    IssueCreator,
    IssueFinder,
    IssueDeleter,
    IssueStageHandler,
)
from tools.kanbans_tools import KanbanFinder
from tools.config_reader import ConfigReader
from tools.xml_tools import update_xml_attribute

ns = api.namespace(
    "resources/kanbans/",
    description="Operations related to issues located in management module",
)
issue_model = api.model(
    "Issue Model",
    {
        "name": fields.String(required=True, description="Issue name"),
        "description": fields.String(required=False, description="Issue description"),
        "creator": fields.String(
            required=False, description="User-creator of the issue"
        ),
    },
)

config = ConfigReader()


@ns.route("/<int:kanban_id>/issues")
class IssuesAll(Resource):
    """ Endpoints for issues """

    @api.response(200, "Issues for kanban board fetched")
    @api.response(500, "Unable to fetch issues")
    def get(self, kanban_id):
        """ Return all issues info for given kanban board """
        kanban_finder = KanbanFinder()
        kanban_directory, kanban_check = kanban_finder.find_kanban_dir_with_id(
            kanban_id=kanban_id, kanbans_directory=config.kanbans_directory
        )
        if kanban_check:
            issue_finder = IssueFinder()
            try:
                all_issues_info_list = issue_finder.return_all_issues_info_for_kanban(
                    kanbans_directory=config.kanbans_directory, kanban_id=kanban_id
                )
                response = jsonify(all_issues_info_list)
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response
            except Exception as e:
                return {"response": "Couldn't fetch issues", "exception": str(e)}, 500
        else:
            return {
                "response": "Couldn't fetch issues",
                "exception": f"Kanban with id {kanban_id} not found",
            }, 404

    @ns.expect(issue_model)
    @api.response(201, "Issue has been created")
    @api.response(500, "Unable to create issue")
    def post(self, kanban_id):
        """ Create new issue for given kanban board """
        issue_creator = IssueCreator()
        issue_xml_tree = issue_creator.create_xml_tree_for_issue_config(
            issue_name=api.payload["name"],
            kanban_id=kanban_id,
            issue_description=api.payload["description"],
            creator=api.payload["creator"],
        )
        try:
            issues_directory = issue_creator.create_issues_folder(
                kanbans_directory=config.kanbans_directory, kanban_id=kanban_id
            )
        except Exception as e:
            return {
                "response": "Unable to create issues directory!",
                "exception": str(e),
            }, 500
        try:
            issue_creator.create_new_issue_config(
                kanbans_directory=config.kanbans_directory,
                kanban_id=kanban_id,
                issues_directory=issues_directory,
                issue_name=api.payload["name"],
                xml_tree=issue_xml_tree,
            )
            return {
                "response": f"Issue with name {api.payload['name']} for kanban with id {kanban_id} created!"
            }, 201
        except Exception as e:
            return {"response": "Unable to create new issue!", "exception": str(e)}, 500


@ns.route("/<int:kanban_id>/issues/<string:issue_name>")
class IssueSingle(Resource):
    """ Endpoints for specifig issues """

    @api.response(200, "Issues for kanban board fetched")
    @api.response(404, "Issue not found")
    @api.response(500, "Unable to fetch issues")
    def get(self, kanban_id, issue_name):
        """ Return specific issue info with given name for given kanban board """
        issue_finder = IssueFinder()
        try:
            (
                issue_directory,
                issue_found,
            ) = issue_finder.return_specific_issue_for_kanban(
                kanbans_directory=config.kanbans_directory,
                kanban_id=kanban_id,
                issue_name=issue_name,
            )
            if issue_found:
                issue_info_list = issue_finder.return_issue_info(
                    issue_directory=issue_directory
                )
                response = jsonify(issue_info_list)
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response
            else:
                return {"response": f"Issue with name {issue_name} not found!"}, 404
        except Exception as e:
            return {"response": "Unable to fetch issue!", "exception": str(e)}

    @api.response(200, "Issues updated")
    @api.response(404, "Issue not found")
    @api.response(500, "Unable update issue")
    @ns.expect(issue_model)
    def put(self, kanban_id, issue_name):
        """ Updates specific issue with given attributes """
        response = dict()
        issue_finder = IssueFinder()
        issue_creator = IssueCreator()
        issue_directory, issue_found = issue_finder.return_specific_issue_for_kanban(
            kanbans_directory=config.kanbans_directory,
            kanban_id=kanban_id,
            issue_name=issue_name,
        )

        if issue_found:
            try:
                if api.payload["name"] != "string":
                    update_xml_attribute(issue_directory, "name", api.payload["name"])
                    issue_creator.rename_issue(
                        issue_directory, issue_name, api.payload["name"]
                    )
                    response["response_name"] = f"Updated with {api.payload['name']}"
                if api.payload["description"] != "string":
                    update_xml_attribute(
                        issue_directory, "description", api.payload["description"]
                    )
                    response[
                        "response_desc"
                    ] = f"Updated with {api.payload['description']}"
                if api.payload["creator"] != "string":
                    update_xml_attribute(
                        issue_directory, "creator", api.payload["creator"]
                    )
                    response["response_desc"] = f"Updated with {api.payload['creator']}"
            except KeyError:
                return {"response": "Wrong key! Use given model"}, 500
            except Exception as e:
                return {"response": "Couldn't update issue", "exception": e}, 500

            return response, 201
        else:
            return {"response": f"Issue with name {issue_name} not found!"}, 404

    @api.response(200, "Issue deleted")
    @api.response(404, "Issue not found")
    @api.response(500, "Unable to delete issue")
    def delete(self, kanban_id, issue_name):
        """ Deletes given issue from given kanban """
        try:
            issue_deleter = IssueDeleter()
            issue_deleter.delete_issue(
                kanbans_directory=config.kanbans_directory,
                kanban_id=kanban_id,
                issue_name=issue_name,
            )
            return {"response": "Issue deleted"}, 200
        except FileNotFoundError:
            return {"response": "Issue coulnd't be found"}, 404
        except Exception as e:
            return {"response": "Couldn't delete issue", "exception": str(e)}, 500


@ns.route("//<int:kanban_id>/issues/<string:issue_name>/stage")
class IssueSingleStage(Resource):
    """ Endpoint for getting stage of certain issue"""
    def get(self, kanban_id, issue_name):
        """ Check on which stage issue is """
        issue_stage_hand = IssueStageHandler()
        try:
            stage = issue_stage_hand.check_stage(
                kanbans_directory=config.kanbans_directory,
                kanban_id=kanban_id,
                issue_name=issue_name,
            )
            return {"response": "Stage for issue fetched", "stage": stage}, 200
        except AttributeError:
            return {"response": "Issue is not set to any stage"}, 500
        except FileNotFoundError:
            return {"response": "Issue coulnd't be found"}, 404
        except Exception as e:
            return {"response": "Couldn't delete issue", "exception": str(e)}, 500


@ns.route("/<int:kanban_id>/issues/<string:issue_name>/<string:stage>")
class IssueSingleStageChange(Resource):
    """ Endpoints for changing issue-stage relation """
    def put(self, kanban_id, issue_name, stage):
        """ Assings chosen issue to given stage """
        issue_stage_hand = IssueStageHandler()
        if (
            issue_stage_hand.check_stage(
                kanbans_directory=config.kanbans_directory,
                kanban_id=kanban_id,
                issue_name=issue_name,
            )
            == stage
        ):
            return {"response": f"Issue {issue_name} already assign to {stage}"}
        try:
            issue_stage_hand.change_stage(
                kanbans_directory=config.kanbans_directory,
                kanban_id=kanban_id,
                issue_name=issue_name,
                stage_to_assign=stage,
            )
        except FileNotFoundError:
            return {"response": f"Kanban with id {kanban_id} doesn't exits"}, 404
        except Exception as e:
            return {"response": "Couldn't assing to stage", "exception": str(e)}, 500
        return 200
