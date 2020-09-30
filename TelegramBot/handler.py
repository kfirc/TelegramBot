from functools import partial, wraps

from telegram.ext import CommandHandler, MessageHandler, InlineQueryHandler


class HandlerDecorator:
    HANDLER_CLASSES = {
        'command': CommandHandler,
        'message': MessageHandler,
        'inline_query': InlineQueryHandler,
    }

    def __init__(self, dispatcher, logger):
        self._dispatcher = dispatcher
        self._logger = logger

    def _handler_decorator(self, handler_class, *args, **kwargs):
        def handler_decorator(handler_func):
            self.add(handler_func, handler_class, *args, **kwargs)
            return handler_func
        return handler_decorator

    def __getattr__(self, item):
        return partial(self._handler_decorator, self.HANDLER_CLASSES[item])

    def add(self, handler_func, handler_class, *args, **kwargs):
        group = kwargs.pop('group', 0)
        add_first = kwargs.pop('add_first', False)
        if issubclass(handler_class, CommandHandler) and not args and not kwargs.get('command'):
            kwargs['command'] = handler_func.__name__

        @wraps(handler_func)
        def logging_wrapper(update, context):
            self._logger.info(f"Request handled by '{handler_func.__name__}' ({update.effective_chat.id})")
            return handler_func(update, context)
        kwargs['callback'] = logging_wrapper

        handler = handler_class(*args, **kwargs)
        self._dispatcher.add_handler(handler, group=group)

        if add_first:
            self._dispatcher.handlers[group].insert(0, self._dispatcher.handlers[group].pop())

    def add_first(self, *args, **kwargs):
        return self.add(add_first=True, *args, **kwargs)
