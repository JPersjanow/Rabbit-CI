import logging
import os


def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s:%(lineno)s - %(message)s')

    # uncomment to get log entries in the console
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    try:
        os.remove("RabbitFramework.log")
    except OSError:
        pass
    file_handler = logging.FileHandler("RabbitFramework.log")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(file_handler)
    return logger