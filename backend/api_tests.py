from flask import Flask, jsonify
from flask_restplus import Resource, Api
from glob import glob
import xmltodict
import os
from directory_creator import DirectoryCreator

api = Api(version='0.1', title='Rabbit-CI API',description='This is a REST API for Rabbit-CI')
directory_creator = DirectoryCreator()

@api.route('/v1/resources/kanbans/all')
class Kanbans(Resource):
    def get(self):
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
