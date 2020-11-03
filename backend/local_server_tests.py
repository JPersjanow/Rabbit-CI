from flask import Flask, request, jsonify
from glob import glob
import xml.etree.cElementTree as ET
from xml.dom import minidom
import xmltodict
import os
import sys
import log

class DirectoryCreator:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.logger = log.Logger('dir_creator').log

        self.kanban_directory = None
    

    def create_directory_tree(self):
        self.logger.info("Creating directory")

        self.logger.info("Creating kanban directory")
        try:
            self.kanban_directory = os.path.join(self.current_dir, 'kanbans')
            os.mkdir(self.kanban_directory, mode=0o777)
            self.logger.info(f"Kanban directory created in {self.kanban_directory}")
        except FileExistsError:
            self.logger.warning(f"{self.kanban_directory} already exists!")
        except Exception as e:
            self.logger.exception(e)

    def prettify(self, elem):
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    ### TESTING PURPOSES ###
    def create_fake_kanbans(self, num_kanbans: int):
        self.logger.debug("Creating fake kanban directories!")
        for i in range(1, num_kanbans, 1):
            self.logger.debug(f"Creating kanban num {i}")
            single_kanban = os.path.join(self.kanban_directory, str(i))
            try:
                os.mkdir(single_kanban, mode=0o777)
            except FileExistsError:
                self.logger.warning(f"{single_kanban} already exists!")
            except Exception as e:
                self.logger.exception(e)

            self.logger.debug("Creating config.xml files")
            try:
                root = ET.Element("kanban")
                info = ET.SubElement(root, "info")
                ET.SubElement(info, "name").text = f"kanban_{str(i)}"
                ET.SubElement(info, "id").text = f"{str(i)}"
                for j in range(10):
                    issues = ET.SubElement(info, "issues")
                    ET.SubElement(issues, "name").text = f"ISS-{j}"
                    ET.SubElement(issues, "creation_date").text = f"03/11/2020"
                    ET.SubElement(issues, "id").text = str(j)
                tree = self.prettify(root)
                with open(os.path.join(single_kanban,"config.xml",), "w+") as file:
                    file.write(tree)
            except Exception as e:
                self.logger.exception(e)



class BackendServer:
    def __init__(self, kanban_directory: str):
        self.app = Flask(__name__)
        self.logger = log.Logger('backend_server').log
        self.kanban_directory = kanban_directory

    def start(self):
        @self.app.route('/hello', methods=['GET'])
        def home():
            if request.method == 'GET':
                return "<h1>Rabbit API v1</h1><p>This site is a prototype API for Rabbit-CI.</p>"

        @self.app.route('/api/v1/resources/kanbans/all', methods=['GET'])
        def api_kanbans_all():
            all_kanbans = glob(f"{self.kanban_directory}/*",recursive=True)
            all_kanbans_info_list = []
            print(all_kanbans)
            for single_kanban_dir in all_kanbans:
                single_kanban_config_file = os.path.join(single_kanban_dir, "config.xml")
                with open(single_kanban_config_file) as xml_file:
                    all_kanbans_info_list.append(xmltodict.parse(xml_file.read()))

            response = jsonify(all_kanbans_info_list)
            response.headers.add("Access-Control-Allow-Origin", "*") # CORE ALLOWANCE!!!!!
            return response

        self.app.run(debug=True)


if __name__ == '__main__':
    d = DirectoryCreator()
    print(d.current_dir)
    d.create_directory_tree()
    d.create_fake_kanbans(num_kanbans=5)
    b = BackendServer(d.kanban_directory)
    b.start()
