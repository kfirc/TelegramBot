import logging
from os import environ

from TelegramBot.utils import classproperty, Singleton


class CustomLogger(metaclass=Singleton):
    def __init__(self):
        # Create a custom logger
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(self.config['level'])
        self.init_env()
        self._logger.info('Telegram Logger initiated')

    @property
    def config(self):
        logging_config = dict(
            level=logging.INFO,
            format='%(asctime)s :: %(levelname)s :: %(message)s',
        )
        if logger_path := environ.get('LOGGER_PATH'):
            logging_config['filename'] = logger_path
        return logging_config

    @property
    def formatter(self):
        return logging.Formatter(self.config['format'])

    def init_env(self):
        if self.support_stream:
            c_handler = logging.StreamHandler()
            c_handler.setLevel(self.config['level'])
            c_handler.setFormatter(self.formatter)
            self._logger.addHandler(c_handler)

        if self.support_files:
            f_handler = logging.FileHandler(self.config['filename'])
            f_handler.setLevel(self.config['level'])
            f_handler.setFormatter(self.formatter)
            self._logger.addHandler(f_handler)

    @classproperty
    def support_files(cls):
        return bool(environ.get('LOGGER_PATH'))

    @classproperty
    def support_stream(cls):
        return environ.get('LOGGER_STREAM', 'true').lower() != 'false'

    def __getattr__(self, item):
        return getattr(self._logger, item)
