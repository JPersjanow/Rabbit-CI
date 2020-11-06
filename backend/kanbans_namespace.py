from flask_restplus import Resource, fields
from flask import jsonify
from glob import glob
import xmltodict
import os

from tools.xml_tools import update_xml_attribute, create_xml_tree_for_kanban_config
from tools.config_reader import ConfigReader
from api import api

ns = api.namespace('resources/kanbans', description='Operations related to kanban boards located in management module')
kanban_update_model = api.model('Kanban Update', {
    'name': fields.String(required=True, description='Kanban name')
})
kanban_create_model = api.clone('Kanban Creation', kanban_update_model, {
    'description': fields.String(required=True, description='Kanban description')
})

config = ConfigReader()

@ns.route('/')
class KanbansAll(Resource):
    @api.response(200, "Kanban boards fetched")
    def get(self):
        """Returns all kanban boards with info"""
        all_kanbans = glob(f"{config.kanban_directory}/*",recursive=True)
        all_kanbans_info_list = []
        print(all_kanbans)
        for single_kanban_dir in all_kanbans:
            single_kanban_config_file = os.path.join(single_kanban_dir, "config.xml")
            with open(single_kanban_config_file) as xml_file:
                all_kanbans_info_list.append(xmltodict.parse(xml_file.read()))
        
        response = jsonify(all_kanbans_info_list)
        response.headers.add("Access-Control-Allow-Origin", "*")

        return response
    
    @ns.expect(kanban_create_model)
    @api.response(201, "New kanban board created")
    @api.response(500, "Kanban could not be created")
    def post(self):
        """Create new kanban"""
        all_kanbans = glob(f"{config.kanban_directory}/*",recursive=True)
        try:
            new_kanban_dir = os.path.join(config.kanban_directory, str(len(all_kanbans) + 1))
            os.mkdir(new_kanban_dir,  mode=0o777)
        except FileExistsError:
            return {"response": "Kanban could not be created! Kanban already exists"}, 500
        except Exception as e:
            return {"response": "Kanban could not be created!", "exception": str(e)}, 500
        try:
                config_tree = create_xml_tree_for_kanban_config(kanban_name=api.payload['name'], kanban_id=len(all_kanbans)+1, description=api.payload['description'])
                with open(os.path.join(new_kanban_dir,"config.xml",), "w+") as file:
                    file.write(config_tree)
        except Exception as e:
            os.rmdir(new_kanban_dir)
            return {"response": "Failed while creating config.xml file, deleting kanban.", "exception": str(e)}, 500

        return {"response": f"New kanban board with id {len(all_kanbans) + 1} created"}
        

@ns.route('/<int:kanban_id>')
class KanbanSingle(Resource):

    @api.response(200, "Kanban board found")
    @api.response(404, "Kanban board with id not found")
    def get(self, kanban_id):
        """Returns kanban board with given id"""
        all_kanbans = glob(f"{config.kanban_directory}/*",recursive=True)
        for kanban_directory in all_kanbans:
            info = os.path.split(kanban_directory)
            if str(kanban_id) in info:
                found = kanban_directory
                break
        if 'found' in locals():
            kanban_config_file = os.path.join(found, "config.xml")
            with open(kanban_config_file) as xml_file:
                kanban_info_list = xmltodict.parse(xml_file.read())
            response = jsonify(kanban_info_list)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        else:
            return {"response": f"Kanban board with id {kanban_id} not found"}, 404

    @ns.expect(kanban_update_model)
    # @ns.marshal_with(kanban) THIS IS RETURNED
    def put(self, kanban_id):
        """Updates name of kanban board with given id"""
        all_kanbans = glob(f"{config.kanban_directory}/*",recursive=True)
        for kanban_directory in all_kanbans:
            info = os.path.split(kanban_directory)
            if str(kanban_id) in info:
                found = kanban_directory
                break
        
        if 'found' in locals():
            print(os.path.join(found, 'config.xml'))
            config_file_dir = os.path.join(found, 'config.xml')
            update_xml_attribute(config_file_dir, 'name', api.payload['name'])

            return {"response": f"Updated with {api.payload['name']}"}

        else:
            return {"response": f"Kanban board with id {kanban_id} not found"}, 404