from flask_restplus import Resource, reqparse, fields
from glob import glob
import xmltodict
from flask import jsonify, request
import os
import xml.etree.cElementTree as ET


from api import api, directory_creator

ns = api.namespace('resources/kanbans', description='Operations related to kanban boards located in management module')
kanban_create_model = api.model('Kanban Creation', {
    'name': fields.String(required=True, description='Kanban name')
})
@ns.route('/')
class KanbansAll(Resource):
    @api.response(200, "Kanban boards fetched")
    def get(self):
        """Returns all kanban board with info"""
        all_kanbans = glob(f"{directory_creator.kanban_directory}/*",recursive=True)
        all_kanbans_info_list = []
        print(all_kanbans)
        for single_kanban_dir in all_kanbans:
            single_kanban_config_file = os.path.join(single_kanban_dir, "config.xml")
            with open(single_kanban_config_file) as xml_file:
                all_kanbans_info_list.append(xmltodict.parse(xml_file.read()))
        
        response = jsonify(all_kanbans_info_list)
        response.headers.add("Access-Control-Allow-Origin", "*")

        return response

@ns.route('/<int:kanban_id>')
class KanbanSingle(Resource):

    @api.response(200, "Kanban board found")
    @api.response(404, "Kanban board with id not found")
    def get(self, kanban_id):
        """Returns kanban board with given id"""
        all_kanbans = glob(f"{directory_creator.kanban_directory}/*",recursive=True)
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

    @ns.expect(kanban_create_model)
    # @ns.marshal_with(kanban) THIS IS RETURNED
    def put(self, kanban_id):
        """Updates kanban board with given id"""
        all_kanbans = glob(f"{directory_creator.kanban_directory}/*",recursive=True)
        for kanban_directory in all_kanbans:
            info = os.path.split(kanban_directory)
            if str(kanban_id) in info:
                found = kanban_directory
                break
        
        if 'found' in locals():
            print(os.path.join(found, 'config.xml'))
            tree = ET.parse(os.path.join(found, 'config.xml'))
            root = tree.getroot()
            for kanban in root:
                kanban.find('name').text = api.payload['name']
            tree.write(os.path.join(found, 'config.xml'))
            return {"response": f"Updated with {api.payload['name']}"}

        else:
            return {"response": f"Kanban board with id {kanban_id} not found"}, 404