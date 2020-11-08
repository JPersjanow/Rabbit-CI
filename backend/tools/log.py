import logging


def setup_custom_logger(name):
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(module)s:%(lineno)s - %(message)s"
    )

    # uncomment to get log entries in the console
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    file_handler = logging.FileHandler("rabbit.log")
    file_handler_custom = logging.FileHandler(f"{name}.log")
    file_handler.setFormatter(formatter)
    file_handler_custom.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    file_handler_custom.setLevel(logging.DEBUG)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(file_handler)
    logger.addHandler(file_handler_custom)
    return logger
