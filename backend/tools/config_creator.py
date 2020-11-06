import xml.etree.cElementTree as ET
from xml_tools import prettify
import os
import sys
from log import setup_custom_logger

class ConfigCreator:
    """ Class for creating config file used by all Rabbit infrastructure"""
    def __init__(self, installation_directory: str, config_directory: str=os.environ['RABBITCONFIG']):
        self.installation_directory = installation_directory
        self.config_directory = config_directory
        self.logger = setup_custom_logger('config_creator')

    def create_config_file(self):
        self.logger.info(f"Creating config file in {self.config_directory}")
        self.logger.info(f"Checking if {self.config_directory} exists")

        check_condfig_dir = os.path.isdir(self.config_directory)
        if check_condfig_dir:
            self.logger.info("Directory exists")
        else:
            self.logger.error("Directory does not exist!")
            sys.exit(1)
        try:
            root = ET.Element("rabbit_config")
            ET.SubElement(root, "installation_directory").text = self.installation_directory
            ET.SubElement(root, "kanban_directory").text = os.path.join(self.installation_directory, 'kanbans')
            tree = prettify(root)
            with open(os.path.join(self.config_directory,"config.xml"), "w+") as file:
                file.write(tree)
        except Exception as e:
            self.logger.exception(e)
        