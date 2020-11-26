import xml.etree.cElementTree as ET
from pathlib import Path
import os
import sys
import argparse
import platform


from tools.log import setup_custom_logger
from tools.xml_tools import prettify
from tools.config_creator import ConfigCreator


class DirectoryCreator:
    """ Main class for creating directory strucute for Rabbit-CI """

    description = "directory_creator.py is a automation script for creating Rabbit-CI directory structure"

    def __init__(self):
        args = self._parse_args(args=sys.argv[1:])
        self.platform = self.check_platform()
        self.installation_directory = self.set_installation_directory(
            args.installation_directory, "default"
        )

        self.logger = setup_custom_logger("directory_creator")

        # MANAGEMENT module
        self.kanban_directory = os.path.join(self.installation_directory, "kanbans")
        self.config_directory = os.path.join(self.installation_directory, "config")
        self.log_directory = os.path.join(self.installation_directory, "logs")

        # AUTOMATION module
        self.jobs_directory = os.path.join(self.installation_directory, "jobs")

        if args.debug == "enable":
            self.debug = True
        else:
            self.debug = False

        if args.validate_directory == "enable":
            self.validate_directory = True
        else:
            self.validate_directory = False

    @staticmethod
    def check_platform() -> str:
        return platform.system()

    @staticmethod
    def set_installation_directory(
        installation_dir_arg: str, default_attribute: str
    ) -> str:
        if installation_dir_arg != default_attribute:
            return installation_dir_arg
        elif installation_dir_arg == default_attribute:
            home = str(Path.home())
            return os.path.join(home, "rabbit")

    @staticmethod
    def _parse_args(args: list) -> argparse.Namespace:
        """
        Arguments parser
        :param args: list as taken from sys.argv
        :return: parsed args
        """
        parser = argparse.ArgumentParser(description=DirectoryCreator.description)
        parser.add_argument(
            "--installation_directory",
            help="Directory where folder structure will be created, if default is set Rabbit will be installed to user home directory",
            default="default",
        )
        parser.add_argument(
            "--debug",
            help="Trun on debug mode. If this mode is enabled, directories will be populated with mock files",
            choices=["enable", "disable"],
            default="disable",
        )
        parser.add_argument(
            "--validate_directory",
            help="If this option is enabled, directory creator will only validate if folder structure is proper",
            choices=["enable", "disable"],
            default="disable",
        )
        parser.add_argument(
            "--exit_on_error",
            help="If this mode is enabled, directory creator will exit if given directories already exits",
            choices=["enable", "disable"],
            default="disable",
        )
        return parser.parse_args(args)

    def create_directory_tree(self):
        self.logger.info(f"Creating main directory in {self.installation_directory}")
        try:
            os.mkdir(self.installation_directory)
            self.logger.info(f"Kanban directory created in {self.kanban_directory}")
        except FileExistsError:
            self.logger.warning(f"{self.kanban_directory} already exists!")
        except Exception as e:
            self.logger.exception(e)

        self.logger.info(
            f"Creating directory structure in {self.installation_directory}"
        )
        self.logger.info("Creating kanban directory")
        try:
            os.mkdir(self.kanban_directory)
            self.logger.info(f"Kanban directory created in {self.kanban_directory}")
        except FileExistsError:
            self.logger.warning(f"{self.kanban_directory} already exists!")
        except Exception as e:
            self.logger.exception(e)

        self.logger.info("Creating config directory")
        try:
            os.mkdir(self.config_directory)
            self.logger.info(f"Config directory created in {self.config_directory}")
            self.logger.info("Setting config directory as environment variable")
            self.set_config_env_variable()
        except FileExistsError:
            self.logger.warning(f"{self.config_directory} already exists!")
        except Exception as e:
            self.logger.exception(e)

        self.logger.info("Creating log directory")
        try:
            os.mkdir(self.log_directory)
            self.logger.info(f"Config directory created in {self.log_directory}")
        except FileExistsError:
            self.logger.warning(f"{self.log_directory} already exists!")
        except Exception as e:
            self.logger.exception(e)

        self.logger.info("Creating jobs directory")
        try:
            os.mkdir(self.jobs_directory)
            self.logger.info(f"Jobs directory created in {self.jobs_directory}")
        except FileExistsError:
            self.logger.warning(f"{self.jobs_directory} already exists!")
        except Exception as e:
            self.logger.exception(e)

    def set_config_env_variable(self):
        if self.platform == "Linux":
            self.logger.info("Linux platform detected")
            with open(os.path.expanduser("~/.bashrc"), "a") as outfile:
                outfile.write(f"export RABBITCONFIG={self.config_directory}")
        elif self.platform == "Windows":
            self.logger.info("Windows platform detected")
            os.system(f"setx RABBITCONFIG {self.config_directory}")

    def create_config_file(self):
        cfg_creator = ConfigCreator(
            installation_directory=self.installation_directory,
            config_directory=self.config_directory,
            kanbans_directory=self.kanban_directory,
            log_directory=self.log_directory,
        )
        cfg_creator.create_config_file()

    def move_log(self):
        os.rename(
            "directory_creator.log",
            os.path.join(self.installation_directory, "logs", "directory_creator.log"),
        )

    def run(self):
        if not self.validate_directory:
            self.create_directory_tree()
            self.create_config_file()
            self.move_log()

        if self.debug:
            self.create_fake_kanbans(num_kanbans=10)

    ### DEBUG METHODS ###
    def create_fake_kanbans(self, num_kanbans: int):
        self.logger.debug("Creating fake kanban directories!")
        for i in range(1, num_kanbans, 1):
            self.logger.debug(f"Creating kanban num {i}")
            single_kanban = os.path.join(self.kanban_directory, str(i))
            try:
                os.mkdir(single_kanban)
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
                tree = prettify(root)
                with open(os.path.join(single_kanban, "config.xml"), "w+") as file:
                    file.write(tree)
            except Exception as e:
                self.logger.exception(e)


if __name__ == "__main__":
    dc = DirectoryCreator()
    dc.run()
