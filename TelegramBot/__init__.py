from os import environ

from telegram.ext import Updater, CommandHandler

from TelegramBot.handler import HandlerDecorator
from TelegramBot.utils.logger import CustomLogger


class TelegramBot:
    def __init__(
            self,
            help_description: str = '',
    ):
        self.help_description = help_description

        self._validate_environ()

        self._logger = CustomLogger()

        self._updater = Updater(token=environ['TELEGRAM_TOKEN'], use_context=True)
        self._dispatcher = self._updater.dispatcher
        self._logger.info('Dispatcher initiated')

        self.handle = HandlerDecorator(self._dispatcher)

    def _validate_environ(self):
        for key in ('TELEGRAM_TOKEN',):
            if key not in environ:
                raise NotImplementedError(f"'{key}' environment variable must be specified")

    def start_polling(self):
        for command in ('start', 'help'):
            if command not in self.all_commands:
                self.handle.add_first(
                    handler_class=CommandHandler,
                    handler_func=self.help,
                    command=command,
                    group=0,
                )

        self._updater.start_polling()
        self._logger.info('Bot is ready and listening')

        try:
            self._updater.idle()
        finally:
            self._logger.info('Bot is offline')

    @property
    def all_handlers(self):
        return [handler for group in self._dispatcher.handlers.values() for handler in group]

    @property
    def all_commands(self):
        return [
            command for handler in self.all_handlers if isinstance(handler, CommandHandler)
            for command in handler.command
        ]

    @property
    def help_string(self):
        string = f'{self.help_description}\n\n'
        command_handlers = [
            handler for handler in self.all_handlers
            if isinstance(handler, CommandHandler)
            and handler.command and not {'help', 'start'}.intersection(set(handler.command))
        ]
        for handler in command_handlers:
            string += f"{' '.join([fr'/{command}' for command in handler.command])} - {handler.callback.__doc__}\n"
        return string

    def help(self, update, context):
        """Help method"""

        context.bot.send_message(chat_id=update.effective_chat.id, text=self.help_string)
