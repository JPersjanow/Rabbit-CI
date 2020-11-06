import xml.etree.cElementTree as ET
import os
import sys
import argparse


from tools.log import setup_custom_logger
from tools.xml_tools import prettify
from tools.config_creator import ConfigCreator

class DirectoryCreator:
    """ Main class for creating directory strucute for Rabbit-CI """
    description = 'directory_creator.py is a automation script for creating Rabbit-CI directory structure'

    def __init__(self):
        args = self._parse_args(args=sys.argv[1:])
        self.installation_directory = args.installation_directory
        self.logger = setup_custom_logger('directory_creator')

        self.kanban_directory = os.path.join(self.installation_directory, 'kanbans')
        self.config_directory = os.path.join(self.installation_directory, 'config') 

        if args.debug == 'enable':
            self.debug = True
        else:
            self.debug = False

        if args.validate_directory == 'enable':
            self.validate_directory = True
        else:
            self.validate_directory = False

    @staticmethod
    def _parse_args(args: list) -> argparse.Namespace:
        """
        Arguments parser
        :param args: list as taken from sys.argv
        :return: parsed args
        """
        parser = argparse.ArgumentParser(description=DirectoryCreator.description)
        parser.add_argument('--installation_directory', help="Directory where folder structure will be created", required=True )
        parser.add_argument('--debug', help="Trun on debug mode. If this mode is enabled, directories will be populated with mock files", choices=['enable', 'disable'], default='disable')
        parser.add_argument('--validate_directory', help="If this option is enabled, directory creator will only validate if folder structure is proper", choices=['enable', 'disable'], default='disable')
        parser.add_argument('--exit_on_error', help="If this mode is enabled, directory creator will exit if given directories already exits", choices=['enable', 'disable'], default='disable')
        return parser.parse_args(args)

    def create_directory_tree(self):
        self.logger.info(f"Creating directory structure in {self.installation_directory}")
        self.logger.info("Creating kanban directory")
        try:
            os.mkdir(self.kanban_directory, mode=0o777)
            self.logger.info(f"Kanban directory created in {self.kanban_directory}")
        except FileExistsError:
            self.logger.warning(f"{self.kanban_directory} already exists!")
        except Exception as e:
            self.logger.exception(e)

        self.logger.info("Creating config directory")
        try:
            os.mkdir(self.config_directory, mode=0o777)
            self.logger.info(f"Config directory created in {self.config_directory}")
            self.logger.info("Setting config directory as environment variable")
            with open(os.path.expanduser('~/.bashrc'), 'a') as outfile:
                outfile.write(f'export RABBITCONFIG={self.config_directory}')
        except FileExistsError:
            self.logger.warning(f"{self.config_directory} already exists!")
        except Exception as e:
            self.logger.exception(e)

    def create_config_file(self):
        cfg_creator = ConfigCreator(installation_directory=self.installation_directory, config_directory=self.config_directory)
        cfg_creator.create_config_file()

    def run(self):
        if not self.validate_directory:
            self.create_directory_tree()
            self.create_config_file()

        if self.debug:
            self.create_fake_kanbans(num_kanbans=10)
            self.create_fake_issues(10, 1)

    ### DEBUG METHODS ###
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
                # for j in range(10):
                #     issues = ET.SubElement(info, "issues")
                #     ET.SubElement(issues, "name").text = f"ISS-{j}"
                #     ET.SubElement(issues, "creation_date").text = f"03/11/2020"
                #     ET.SubElement(issues, "id").text = str(j)
                tree = prettify(root)
                with open(os.path.join(single_kanban,"config.xml"), "w+") as file:
                    file.write(tree)
            except Exception as e:
                self.logger.exception(e)
    
    def create_fake_issues(self, num_issues: int, kanban_id: int):
        pass

if __name__ == '__main__':
    dc = DirectoryCreator()
    dc.run()