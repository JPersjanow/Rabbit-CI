from flask_restplus import Resource, fields
from flask import jsonify, request
from api import api, logger

from kanbans_namespace import ns
from tools.issues_tools import (
    IssueCreator,
    IssueFinder,
    IssueUpdater,
    IssueDeleter,
    IssueStageHandler,
    Stages,
)
from tools.kanbans_tools import KanbanFinder
from tools.config_reader import ConfigReader
from tools.xml_tools import update_xml_attribute

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

issue_model_stage = api.model(
    "Issue-stage Model",
    {
        "stage": fields.String(required=True, description="Stage name"),
    },
)

config = ConfigReader()
# PAGINATION
# @ns.route("/issues")
# class Issues(Resource):
#     def get(self):
#         limit = request.args.get("limit")
#         print(limit)


@ns.route("/<int:kanban_id>/issues")
class IssuesAll(Resource):
    """ Endpoints for issues """

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
                return {"response": "Unable to fetch issues"}, 500
        else:
            logger.warning(
                f"Unable to fetch issues! Kanban with id {kanban_id} not found"
            )
            return {"response": "Kanban id not found"}, 400

    @ns.expect(issue_model)
    @api.response(201, "Issue has been created")
    @api.response(400, "Bad request")
    @api.response(500, "Unable to create issue")
    def post(self, kanban_id):
        if (
            api.payload["name"].replace(" ", "") == ""
            or api.payload["creator"].replace(" ", "") == ""
        ):
            return {"response": "Name/creator cannot be null or whitespaces only"}, 400
        logger.info("Creating issue xml config")
        issue_creator = IssueCreator()

        try:
            logger.info("Creating issue directory if needed")
            issue_creator.create_issue_folder(
                kanbans_directory=config.kanbans_directory, kanban_id=kanban_id
            )
        except FileNotFoundError as fe:
            logger.error(
                f"Unable to create issue directory! "
                f"Kanban with id {kanban_id} doesn't exist"
            )
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
                issue_description=api.payload["description"],
                issue_name=api.payload["name"],
                creator=api.payload["creator"],
            )
            return {
                "response": f"Issue with name {api.payload['name']} for kanban with id {kanban_id} created!"
            }, 201
        except FileExistsError as fe:
            logger.warning("Issue already exists!")
            return {
                "response": "Unable to create new issue!",
                "exception": str(fe),
            }, 500
        except Exception as e:
            logger.error("Unable to create issue!")
            logger.exception(e)
            return {"response": "Unable to create new issue!"}, 500


@ns.route("/<int:kanban_id>/issues/<int:issue_id>")
class IssueSingle(Resource):
    """ Endpoints for singular issue """

    @api.response(400, "Bad request")
    @api.response(500, "Unable to fetch issue")
    def get(self, kanban_id, issue_id):
        kanban_finder = KanbanFinder()
        logger.info(f"Fetching kanban directory with id {kanban_id}")
        kanban_directory, kanban_check = kanban_finder.find_kanban_dir_with_id(
            kanban_id=kanban_id, kanbans_directory=config.kanbans_directory
        )
        logger.info(f"Kanban directory {kanban_directory}")
        if kanban_check:
            issue_finder = IssueFinder()
            issues_directory = issue_finder.return_issues_directory_for_kanban(
                kanbans_directory=config.kanbans_directory, kanban_id=kanban_id
            )
            issue_check = issue_finder.check_if_issue_extists(
                issues_directory=issues_directory, issue_id=issue_id
            )
            if issue_check:
                try:
                    logger.info(
                        f"Fetching issues with id {issue_id} for kanban with id {kanban_id}"
                    )
                    issue_info_list = issue_finder.return_issue_info_for_kanban(
                        kanbans_directory=config.kanbans_directory,
                        kanban_id=kanban_id,
                        issue_id=issue_id,
                    )
                    response = jsonify(issue_info_list)
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    return response
                except Exception as e:
                    logger.error("Unable to fetch issues!")
                    logger.exception(e)
                    return {"response": "Unable to fetch issues"}, 500
            else:
                logger.warning(
                    f"Unable to fetch issues! Issue with id {issue_id} not found"
                )
                return {"response": "Issue id not found"}, 400
        else:
            logger.warning(
                f"Unable to fetch issues! Kanban with id {kanban_id} not found"
            )
            return {"response": "Kanban id not found"}, 400

    @ns.expect(issue_model)
    @api.response(204, "Issues updated")
    @api.response(404, "Issue not found")
    @api.response(500, "Unable update issue")
    def put(self, kanban_id, issue_id):
        """ Updates specific issue with given attributes """
        kanban_finder = KanbanFinder()
        logger.info(f"Fetching kanban directory with id {kanban_id}")
        kanban_directory, kanban_check = kanban_finder.find_kanban_dir_with_id(
            kanban_id=kanban_id, kanbans_directory=config.kanbans_directory
        )
        logger.info(f"Kanban directory {kanban_directory}")
        if kanban_check:
            issue_finder = IssueFinder()
            issues_directory = issue_finder.return_issues_directory_for_kanban(
                kanbans_directory=config.kanbans_directory, kanban_id=kanban_id
            )
            issue_check = issue_finder.check_if_issue_extists(
                issues_directory=issues_directory, issue_id=issue_id
            )
            if issue_check:
                issue_updater = IssueUpdater()
                try:
                    if api.payload["description"] != "string":
                        issue_updater.update_issue(
                            issues_directory,
                            issue_id,
                            "description",
                            api.payload["description"],
                        )
                    if api.payload["creator"] != "string":
                        issue_updater.update_issue(
                            issues_directory,
                            issue_id,
                            "creator",
                            api.payload["creator"],
                        )
                    if api.payload["name"] != "string":
                        issue_updater.update_issue(
                            issues_directory, issue_id, "name", api.payload["name"]
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
                logger.warning(
                    f"Unable to update issues! Issue with id {issue_id} not found"
                )
                return {"response": "Issue id not found"}, 400
        else:
            logger.warning(
                f"Unable to fetch issues! Kanban with id {kanban_id} not found"
            )
            return {"response": "Kanban id not found"}, 400

    @api.response(204, "Issue deleted")
    @api.response(400, "Issue not found")
    @api.response(500, "Unable to delete issue")
    def delete(self, kanban_id, issue_id):
        """ Deletes issue for given kanban """
        kanban_finder = KanbanFinder()
        logger.info(f"Fetching kanban directory with id {kanban_id}")
        kanban_directory, kanban_check = kanban_finder.find_kanban_dir_with_id(
            kanban_id=kanban_id, kanbans_directory=config.kanbans_directory
        )
        logger.info(f"Kanban directory {kanban_directory}")
        if kanban_check:
            try:
                issue_deleter = IssueDeleter()
                issue_deleter.delete_issue_for_kanban(
                    kanbans_directory=config.kanbans_directory,
                    kanban_id=kanban_id,
                    issue_id=issue_id,
                )
            except FileNotFoundError as fe:
                logger.warning(
                    f"Unable to update issues! Issue with id {issue_id} not found"
                )
                logger.exception(fe)
                return {"response": "Issue id not found"}, 400
            except Exception as e:
                logger.error("Couldn't update issue")
                logger.exception(e)
                return {"response": "Couldn't update issue"}, 500
            return 204
        else:
            logger.warning(
                f"Unable to fetch issues! Kanban with id {kanban_id} not found"
            )
            return {"response": "Kanban id not found"}, 400


@ns.route("//<int:kanban_id>/issues/<int:issue_id>/stage")
class IssueSingleStage(Resource):
    """ Endpoint for getting stage of certain issue"""

    @api.response(400, "Bad request")
    @api.response(500, "Unable to fetch stage")
    def get(self, kanban_id, issue_id):
        """ Check on which stage issue is """
        issue_stage_hand = IssueStageHandler()
        logger.info(f"Checking issue with id {issue_id} current stage")
        try:
            stage = issue_stage_hand.check_stage(
                kanbans_directory=config.kanbans_directory,
                kanban_id=kanban_id,
                issue_id=issue_id,
            )
            response = jsonify(stage)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        except AttributeError:
            logger.error(f"Issue is not set to any stage! Check issue config xml")
            return {"response": "Issue is not set to any stage"}, 500
        except FileNotFoundError:
            logger.warning("Issue couldn't be found")
            return {"response": "Issue id not found"}, 400
        except Exception as e:
            logger.error("Couldn't check issue stage!")
            logger.exception(e)
            return {"response": "Couldn't check issue stage"}, 500

    @ns.expect(issue_model_stage)
    @api.response(201, "Issue changed")
    @api.response(400, "Bad request")
    @api.response(500, "Unable to change stage")
    def put(self, kanban_id, issue_id):
        if (
            api.payload["stage"].replace(" ", "") == ""
            or api.payload["stage"] == "string"
        ):
            return {"response": "Stage cannot be null or whitespaces only"}, 400

        issue_stage_hand = IssueStageHandler()
        logger.info(f"Changing issue with id {issue_id} current stage")
        try:
            issue_stage_hand.change_stage(
                kanbans_directory=config.kanbans_directory,
                kanban_id=kanban_id,
                issue_id=issue_id,
                stage_to_assign=api.payload["stage"],
            )
            return 201
        except AttributeError:
            logger.error(f"Issue is not set to any stage! Check issue config xml")
            return {"response": "Issue is not set to any stage"}, 500
        except FileNotFoundError:
            logger.warning("Issue couldn't be found")
            return {"response": "Issue id not found"}, 400
        except Exception as e:
            logger.error("Couldn't update issue stage!")
            logger.exception(e)
            return {"response": "Unable to update issue stage"}, 500
