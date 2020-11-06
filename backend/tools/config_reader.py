from tools.log import setup_custom_logger
import os
import xmltodict

class ConfigReader:
    def __init__(self):
        self.config_directory = os.environ['RABBITCONFIG']
        self.installation_directory, self.kanban_directory = self.read()

    def read(self):
        with open(os.path.join(self.config_directory, 'config.xml'), 'r') as config_file:
            config_dict = xmltodict.parse(config_file.read())
        
        return config_dict['rabbit_config']['installation_directory'], config_dict['rabbit_config']['kanban_directory']