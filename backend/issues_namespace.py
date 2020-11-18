from flask_restplus import Resource, fields
from flask import jsonify
from api import api, logger

from tools.issues_tools import (
    IssueCreator,
    IssueFinder,
    IssueDeleter,
    IssueStageHandler,
    Stages
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
    @api.response(400, "Bad request")
    @api.response(500, "Unable to fetch issues")
    def get(self, kanban_id):
        """ Return all issues info for given kanban board """
        kanban_finder = KanbanFinder()
        logger.info(f"Fetching kanban directory with id {kanban_id}")
        kanban_directory, kanban_check = kanban_finder.find_kanban_dir_with_id(
            kanban_id=kanban_id, kanbans_directory=config.kanbans_directory
        )
        logger.info(f"Kanban directory {kanban_directory}")
        if kanban_check:
            issue_finder = IssueFinder()
            try:
                logger.info(f"Fetching all issues for kanban with id {kanban_id}")
                all_issues_info_list = issue_finder.return_all_issues_info_for_kanban(
                    kanbans_directory=config.kanbans_directory, kanban_id=kanban_id
                )
                response = jsonify(all_issues_info_list)
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response
            except Exception as e:
                logger.error("Unable to fetch issues!")
                logger.exception(e)
                return {"response": "Unable to fetch issues", "exception": str(e)}, 500
        else:
            logger.warning(f"Unable to fetch issues! Kanban with id {kanban_id} not found")
            return {"response": "Kanban id not found"}, 400

    @ns.expect(issue_model)
    @api.response(201, "Issue has been created")
    @api.response(400, "Bad request")
    @api.response(500, "Unable to create issue")
    def post(self, kanban_id):
        """ Create new issue for given kanban board """
        issue_creator = IssueCreator()
        if api.payload["name"].replace(" ", "") == "" or api.payload["creator"].replace(" ", "") == "":
            return {"response": "Name/creator cannot be null or whitespaces only"}, 400
        logger.info("Creating issue xml config")
        issue_xml_tree = issue_creator.create_xml_tree_for_issue_config(
            issue_name=api.payload["name"],
            kanban_id=kanban_id,
            issue_description=api.payload["description"],
            creator=api.payload["creator"],
        )
        try:
            logger.info("Creating issue directory if needed")
            issues_directory = issue_creator.create_issues_folder(
                kanbans_directory=config.kanbans_directory, kanban_id=kanban_id
            )
        except FileNotFoundError as fe:
            logger.error(f"Unable to create issue directory! " \
                f"Kanban with id {kanban_id} doesn't exist")
            logger.exception(fe)
            return {"response": "Kanban id not found"}, 400
        except Exception as e:
            logger.error("Unable to create issues directory!")
            logger.exception(e)
            return {"response": "Unable to create issues directory!"}, 500
        try:
            logger.info("Creating new issue")
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
        except FileExistsError as fe:
            logger.warning("Issue already exists!")
            return {"response": "Unable to create new issue!", "exception": str(fe)}, 500
        except Exception as e:
            logger.error("Unable to create issue!")
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
            logger.info(f"Fetching issue {issue_name} directory for kanban with id {kanban_id}")
            (
                issue_directory,
                issue_found,
            ) = issue_finder.return_specific_issue_for_kanban(
                kanbans_directory=config.kanbans_directory,
                kanban_id=kanban_id,
                issue_name=issue_name,
            )
            if issue_found:
                logger.info("Fetching issue info")
                issue_info_list = issue_finder.return_issue_info(
                    issue_directory=issue_directory
                )
                response = jsonify(issue_info_list)
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response
            else:
                logger.warning("Issue not found!")
                return {"response": f"Issue with name {issue_name} not found!"}, 404
        except FileNotFoundError as fe:
            logger.error("Issue info couldn't be fetched!")
            logger.exception(fe)
            return {"response": "Kanban id not found"}, 400
        except Exception as e:
            logger.error("Unable to fetch issue")
            logger.exception(e)
            return {"response": "Unable to fetch issue"}, 500

    @api.response(204, "Issues updated")
    @api.response(404, "Issue not found")
    @api.response(500, "Unable update issue")
    @ns.expect(issue_model)
    def put(self, kanban_id, issue_name):
        """ Updates specific issue with given attributes """
        issue_finder = IssueFinder()
        issue_creator = IssueCreator()
        logger.info(f"Fetching issue {issue_name} directory for kanban with id {kanban_id}")
        issue_directory, issue_found = issue_finder.return_specific_issue_for_kanban(
            kanbans_directory=config.kanbans_directory,
            kanban_id=kanban_id,
            issue_name=issue_name,
        )

        if issue_found:
            try:
                if api.payload["description"] != "string":
                    update_xml_attribute(
                        issue_directory, "description", api.payload["description"]
                    )
                if api.payload["creator"] != "string":
                    update_xml_attribute(
                        issue_directory, "creator", api.payload["creator"]
                    )
                if api.payload["name"] != "string":
                    update_xml_attribute(issue_directory, "name", api.payload["name"])
                    issue_creator.rename_issue(
                        issue_directory, issue_name, api.payload["name"]
                    )
            except KeyError as ke:
                logger.error("Key not matching model used!")
                logger.exception(ke)
                return {"response": "Wrong key! Use given model"}, 500
            except Exception as e:
                logger.error("Couldn't update issue")
                logger.exception(e)
                return {"response": "Couldn't update issue"}, 500

            return 204
        else:
            logger.warning("Issue not found!")
            return {"response": "Issue not found!"}, 404

    @api.response(204, "Issue deleted")
    @api.response(400, "Issue not found")
    @api.response(500, "Unable to delete issue")
    def delete(self, kanban_id, issue_name):
        """ Deletes given issue from given kanban """
        issue_deleter = IssueDeleter()
        logger.info(f"Deleting issue {issue_name} for kanban {kanban_id}")
        try:
            issue_deleter.delete_issue(
                kanbans_directory=config.kanbans_directory,
                kanban_id=kanban_id,
                issue_name=issue_name,
            )
            return {"response": "Issue deleted"}, 204
        except FileNotFoundError:
            logger.warning("Issue couln't be found")
            return {"response": "Issue not found"}, 400
        except Exception as e:
            logger.error("Issue couldn't be deleted!")
            logger.exception(e)
            return {"response": "Unable to delete issue"}, 500


@ns.route("//<int:kanban_id>/issues/<string:issue_name>/stage")
class IssueSingleStage(Resource):
    """ Endpoint for getting stage of certain issue"""
    def get(self, kanban_id, issue_name):
        """ Check on which stage issue is """
        issue_stage_hand = IssueStageHandler()
        logger.info(f"Checking issue {issue_name} current stage")
        try:
            stage = issue_stage_hand.check_stage(
                kanbans_directory=config.kanbans_directory,
                kanban_id=kanban_id,
                issue_name=issue_name,
            )
            return {"response": "Stage for issue fetched", "stage": stage}, 200
        except AttributeError:
            logger.error(f"Issue is not set to any stage! Check issue config xml")
            return {"response": "Issue is not set to any stage"}, 500
        except FileNotFoundError:
            logger.warning("Issue couldn't be found")
            return {"response": "Issue id not found"}, 400
        except Exception as e:
            logger.error("Issue couldn't be deleted!")
            logger.exception(e)
            return {"response": "Couldn't delete issue", "exception": str(e)}, 500


@ns.route("/<int:kanban_id>/issues/<string:issue_name>/<string:stage>")
class IssueSingleStageChange(Resource):
    """ Endpoints for changing issue-stage relation """
    def put(self, kanban_id, issue_name, stage):
        """ Assings chosen issue to given stage """
        issue_stage_hand = IssueStageHandler()
        if stage not in [stage.value for stage in Stages]:
            return {"response": "Stage is not valid"}, 400
        logger.info(f"Assigning issue {issue_name} to new stage")
        logger.info(f"Checking issue {issue_name} current stage")
        try:
            if (
                issue_stage_hand.check_stage(
                    kanbans_directory=config.kanbans_directory,
                    kanban_id=kanban_id,
                    issue_name=issue_name,
                )
                == stage
            ):
                logger.info("No update needed")
                return 204
        except FileNotFoundError:
            logger.warning("Issue or Kanban doesn't exist")
            return {"response": f"Kanban with id {kanban_id} or issue {issue_name} doesn't exits"}, 404
        logger.info(f"Changing issue {issue_name} stage")
        try:
            issue_stage_hand.change_stage(
                kanbans_directory=config.kanbans_directory,
                kanban_id=kanban_id,
                issue_name=issue_name,
                stage_to_assign=stage,
            )
        except FileNotFoundError:
            logger.warning("Issue or Kanban doesn't exist")
            return {"response": f"Kanban with id {kanban_id} or issue {issue_name} doesn't exits"}, 404
        except Exception as e:
            logger.error("Couldn't assign issue to stage")
            logger.exception(e)
            return {"response": "Couldn't assing to stage", "exception": str(e)}, 500
        return 204
