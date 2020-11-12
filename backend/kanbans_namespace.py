import os
from flask_restplus import Resource, fields
from flask import jsonify

from tools.xml_tools import update_xml_attribute
from tools.config_reader import ConfigReader
from tools.kanbans_tools import KanbanFinder, KanbanCreator, KanbanDeleter
from api import api, logger

ns = api.namespace(
    "resources/kanbans",
    description="Operations related to kanban boards located in management module",
)
kanban_model = api.model(
    "Kanban Model",
    {
        "name": fields.String(required=True, description="Kanban name"),
        "description": fields.String(required=True, description="Kanban description"),
    },
)

# Config file reader (from env variable)
config = ConfigReader()


@ns.route("/")
class KanbansAll(Resource):
    """ Endpoints for kanbans """

    @api.response(200, "Kanban boards fetched")
    @api.response(500, "Could not fetch Kanban boards info")
    def get(self):
        """Returns all kanban boards with info"""
        kanban_finder = KanbanFinder()
        logger.info("Fetching all kanbans info")
        try:
            all_kanbans_info_list = kanban_finder.return_all_kanabans_info(
                kanbans_directory=config.kanbans_directory
            )
            print(all_kanbans_info_list)
            response = jsonify(all_kanbans_info_list)
            print(response)
            response.headers.add("Access-Control-Allow-Origin", "*")
        except Exception as e:
            logger.error("Coulnd't fetch kanbans")
            logger.exception(e)
            return {"response": f"Kanbans couldn't be fetched! {e}"}, 500

        return response

    @ns.expect(kanban_model)
    @api.response(201, "New kanban board created")
    @api.response(400, "Bad request")
    @api.response(500, "Kanban could not be created")
    def post(self):
        """Create new kanban"""
        kanban_creator = KanbanCreator()
        logger.info("Creating new kanban")
        if api.payload["name"].replace(" ", "") == "":
            return {"response": "Name cannot be null or whitespaces only"}, 400
        try:
            new_kanban_dir, new_kanban_id = kanban_creator.create_new_kanban_folder(
                kanbans_directory=config.kanbans_directory
            )
        except FileExistsError:
            logger.error("Kanban already exists!")
            return {
                "response": "Unable to create! Kanban already exists"
            }, 500
        except Exception as e:
            logger.error("Couldn't create kanban!")
            logger.exception(e)
            return {
                "response": "Unable to create",
                "exception": str(e),
            }, 500
        try:
            logger.info("Creating config xml for new kanban")
            config_tree = kanban_creator.create_xml_tree_for_kanban_config(
                kanban_name=api.payload["name"],
                kanban_id=new_kanban_id,
                description=api.payload["description"],
            )
            kanban_creator.create_new_kanban_config(
                new_kanban_directory=new_kanban_dir, config_xml_tree=config_tree
            )
        except Exception as e:
            logger.error("Couldn't create new kanban config! Deleting kanban")
            logger.exception(e)
            os.rmdir(new_kanban_dir)
            return {
                "response": "Failed while creating config.xml file, deleting kanban.",
                "exception": str(e),
            }, 500

        return {
            "response": f"New kanban board with id {new_kanban_id} created"
        }, 201


@ns.route("/<int:kanban_id>")
class KanbanSingle(Resource):
    """ Endpoints for specific kanbans """

    @api.response(200, "Kanban board found")
    @api.response(400, "Kanban id not found")
    def get(self, kanban_id):
        """Returns kanban board with given id"""
        kanban_finder = KanbanFinder()
        logger.info(f"Fetching kanban with id {kanban_id} info")
        kanban_directory, kanban_found = kanban_finder.find_kanban_dir_with_id(
            kanban_id=kanban_id, kanbans_directory=config.kanbans_directory
        )

        if kanban_found:
            kanban_info_list = kanban_finder.return_kanban_info(
                kanban_directory=kanban_directory
            )
            response = jsonify(kanban_info_list)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        else:
            logger.warning(f"Kanban with id {kanban_id} not found!")
            return {"response": "Kanban id not found"}, 400

    @ns.expect(kanban_model)
    @api.response(204, "Kanban updated")
    @api.response(400, "Bad request")
    # @ns.marshal_with(kanban) THIS IS RETURNED
    def put(self, kanban_id):
        """Updates kanban board with given id"""
        kanban_finder = KanbanFinder()
        logger.info(f"Updating kanban with id {kanban_id}")
        kanban_directory, kanban_found = kanban_finder.find_kanban_dir_with_id(
            kanban_id=kanban_id, kanbans_directory=config.kanbans_directory
        )
        response = dict()
        if kanban_found:
            config_file_dir = os.path.join(kanban_directory, "config.xml")
            logger.info(config_file_dir)
            try:
                if api.payload["name"].replace(" ", "") == "":
                    return {"response": "Name cannot be null or whitespaces only"}, 400
                elif api.payload["name"] != "string":
                    update_xml_attribute(config_file_dir, "name", api.payload["name"])
                    response["response_name"] = f"Updated with {api.payload['name']}"
                if api.payload["description"] != "string":
                    update_xml_attribute(
                        config_file_dir, "description", api.payload["description"]
                    )
                    response[
                        "response_desc"
                    ] = f"Updated with {api.payload['description']}"
            except KeyError as ke:
                logger.error("Key not matching model used!")
                logger.exception(ke)
                return {"response": "Wrong key! Use given model"}, 400

            return response, 204

        else:
            logger.warning(f"Kanban with id {kanban_id} not found!")
            return {"response": "Kanban id not found"}, 404

    @api.response(204, "Kanban deleted")
    @api.response(400, "Kanban id not found")
    @api.response(500, "Unable to delete kanban")
    def delete(self, kanban_id):
        """ Delete kanban board with given id """
        logger.info(f"Deleting kanban with id {kanban_id}")
        try:
            kanban_deleter = KanbanDeleter()
            kanban_deleter.delete_kanban(
                kanbans_directory=config.kanbans_directory, kanban_id=kanban_id
            )
            return {"response": "Kanban deleted"}, 204
        except FileNotFoundError:
            logger.warning(f"Kanban with id {kanban_id} not found")
            return {"response": "Kanban id not found"}, 400
        except Exception as e:
            logger.error("Unable to delte kanban")
            logger.exception(e)
            return {"response": "Unable to delte kanban", "exception": str(e)}, 500
