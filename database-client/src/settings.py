import logging

log = logging.getLogger(__name__)

class Settings:
    def __init__(self):
        """
        Settings class of which instance should be shared through
        all other classes that need it
        """


        log.info('Program starting')
        log.debug('Loading settings...')
