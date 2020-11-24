from flask_restplus import Api
from tools.log import setup_custom_logger

api = Api(
    version="0.33",
    title="Rabbit-CI API",
    description="This is a REST API for Rabbit-CI",
)
logger = setup_custom_logger("api_server")
