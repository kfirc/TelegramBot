from enum import Enum
from functools import wraps

from telegram.ext import CommandHandler, MessageHandler, InlineQueryHandler, CallbackQueryHandler


def default_handler_custom_wrapper(handler_func):
    return handler_func


def callback_query_handler_custom_wrapper(handler_func):
    @wraps(handler_func)
    def _wrapper(update, context):
        results = handler_func(update, context)
        update.callback_query.answer()
        return results

    return _wrapper


class HandlerClass(Enum):
    command = CommandHandler
    message = MessageHandler
    inline_query = InlineQueryHandler
    callback_query = CallbackQueryHandler

    @property
    def func_name_arg(self):
        return {
            HandlerClass.command: 'command',
            HandlerClass.callback_query: 'pattern',
        }.get(self)

    @property
    def custom_wrapper(self):
        return {
            HandlerClass.callback_query: callback_query_handler_custom_wrapper,
        }.get(self, default_handler_custom_wrapper)
