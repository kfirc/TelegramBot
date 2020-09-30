import logging

from TelegramBot.utils import Singleton


class CustomLogger(metaclass=Singleton):
    def __init__(
            self,
            logger_path=None,
            logger_stream=True,
    ):
        self.logger_path = logger_path
        self.logger_stream = logger_stream

        # Create a custom logger
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(self.config['level'])
        self.init_env()
        self._logger.info('Telegram Logger initiated')

    @property
    def config(self):
        return dict(
            filename=self.logger_path,
            level=logging.INFO,
            format='%(asctime)s :: %(levelname)s :: %(message)s',
        )

    @property
    def formatter(self):
        return logging.Formatter(self.config['format'])

    def init_env(self):
        if self.logger_stream:
            c_handler = logging.StreamHandler()
            c_handler.setLevel(self.config['level'])
            c_handler.setFormatter(self.formatter)
            self._logger.addHandler(c_handler)

        if self.support_files:
            f_handler = logging.FileHandler(self.config['filename'])
            f_handler.setLevel(self.config['level'])
            f_handler.setFormatter(self.formatter)
            self._logger.addHandler(f_handler)

    @property
    def support_files(self):
        return bool(self.config['filename'])

    def __getattr__(self, item):
        return getattr(self._logger, item)
