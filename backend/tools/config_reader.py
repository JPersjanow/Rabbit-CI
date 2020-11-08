import os
import sys
import xmltodict

from tools.log import setup_custom_logger


class ConfigReader:
    """ Class for reading config file used by all Rabbit infrastructure """

    def __init__(self):
        self.logger = setup_custom_logger("config_reader")

        try:
            self.config_directory = os.environ["RABBITCONFIG"]
        except KeyError:
            self.logger.info(
                "Unable to get RABBITCONFIG environmental variable! Exiting"
            )
            sys.exit(1)

        self.installation_directory, self.kanbans_directory = self.read()

    def read(self):
        self.logger.info("Reading config file for rabbit-ci")
        with open(
            os.path.join(self.config_directory, "config.xml"), "r"
        ) as config_file:
            config_dict = xmltodict.parse(config_file.read())

        return (
            config_dict["rabbit_config"]["installation_directory"],
            config_dict["rabbit_config"]["kanbans_directory"],
        )
