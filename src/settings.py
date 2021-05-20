import logging


def info(text):
    logging.info(text)


def debug(text):
    logging.debug(text)


class Settings:
    def __init__(self):
        """
        Settings class of which instance should be shared through
        all other classes that need it
        """
        logging.basicConfig(format='%(levelname)s :: %(message)s', level=logging.DEBUG)

        logging.info('Program starting')
        logging.debug('Loading settings...')
