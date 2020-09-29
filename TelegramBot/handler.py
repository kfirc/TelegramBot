from functools import partial

from telegram.ext import CommandHandler, MessageHandler, InlineQueryHandler


class HandlerDecorator:
    HANDLER_CLASSES = {
        'command': CommandHandler,
        'message': MessageHandler,
        'inline_query': InlineQueryHandler,
    }

    def __init__(self, dispatcher):
        self._dispatcher = dispatcher

    def _handler_decorator(self, handler_class, *args, **kwargs):
        def handler_decorator(handler_func):
            self.add(handler_func, handler_class, *args, **kwargs)
            return handler_func
        return handler_decorator

    def __getattr__(self, item):
        return partial(self._handler_decorator, self.HANDLER_CLASSES[item])

    def add(self, handler_func, handler_class, *args, **kwargs):
        kwargs['callback'] = handler_func
        group = kwargs.pop('group', 0)
        add_first = kwargs.pop('add_first', False)
        if issubclass(handler_class, CommandHandler) and not args and not kwargs.get('command'):
            kwargs['command'] = handler_func.__name__

        handler = handler_class(*args, **kwargs)
        self._dispatcher.add_handler(handler, group=group)

        if add_first:
            self._dispatcher.handlers[group].insert(0, self._dispatcher.handlers[group].pop())

    def add_first(self, *args, **kwargs):
        return self.add(add_first=True, *args, **kwargs)
