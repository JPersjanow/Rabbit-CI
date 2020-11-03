from flask_restplus import Resource, reqparse, fields
from glob import glob
import xmltodict
from flask import jsonify, request
import os
import xml.etree.cElementTree as ET
from xml.dom import minidom


from api import api, directory_creator

# here until code refactor
def prettify(elem):
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")


ns = api.namespace('resources/kanban', description='Operations related to kanban boards located in management module')
kanban_create_model = api.model('Kanban Creation', {
    'name': fields.String(required=True, description='Kanban name')
})
@ns.route('/')
class KanbansAll(Resource):
    @api.response(200, "Kanban boards fetched")
    def get(self):
        """Returns all kanban boards with info"""
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
    
    @ns.expect(kanban_create_model)
    @api.response(201, "New kanban board created")
    @api.response(500, "Kanban could not be created")
    def post(self):
        """Create new kanban"""
        all_kanbans = glob(f"{directory_creator.kanban_directory}/*",recursive=True)
        try:
            new_kanban_dir = os.path.join(directory_creator.kanban_directory, str(len(all_kanbans) + 1))
            os.mkdir(new_kanban_dir,  mode=0o777)
        except FileExistsError:
            return {"response": "Kanban could not be created! Kanban already exists"}, 500
        except Exception as e:
            return {"response": "Kanban could not be created!", "exception": str(e)}, 500
        try:
                root = ET.Element("kanban")
                info = ET.SubElement(root, "info")
                ET.SubElement(info, "name").text = api.payload['name']
                ET.SubElement(info, "id").text = str(len(all_kanbans) + 1)
                for j in range(10):
                    issues = ET.SubElement(info, "issues")
                    ET.SubElement(issues, "name").text = f"ISS-{j}"
                    ET.SubElement(issues, "creation_date").text = f"03/11/2020"
                    ET.SubElement(issues, "id").text = str(j)
                tree = prettify(root)
                with open(os.path.join(new_kanban_dir,"config.xml",), "w+") as file:
                    file.write(tree)
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