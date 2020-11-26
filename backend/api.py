from flask_restplus import Api
from tools.log import setup_custom_logger
from tools.config_reader import ConfigReader
import os

api = Api(
    version="0.35",
    title="Rabbit-CI API",
    description="This is a REST API for Rabbit-CI",
)
config = ConfigReader()
log_directory = os.path.join(config.installation_directory, "logs")
logger = setup_custom_logger(os.path.join(log_directory, "api_server"))
