import logging

class Logger:
    def __init__(self, name: str):
        self.name = name
        self.log = self.setup_logger()

    def setup_logger(self):
        # create logger
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        return logger