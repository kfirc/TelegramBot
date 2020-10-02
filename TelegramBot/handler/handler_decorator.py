from functools import partial, wraps

from TelegramBot.handler.handler_classes import HandlerClass


class HandlerDecorator:
    def __init__(self, dispatcher, logger):
        self._dispatcher = dispatcher
        self._logger = logger

    def _handler_decorator(self, handler_class_name, *args, **kwargs):
        def handler_decorator(handler_func):
            self.add(handler_func, HandlerClass[handler_class_name].value, *args, **kwargs)
            return handler_func
        return handler_decorator

    def __getattr__(self, item):
        return partial(self._handler_decorator, item)

    def add(self, handler_func, handler_class, *args, **kwargs):
        group = kwargs.pop('group', 0)
        add_first = kwargs.pop('add_first', False)
        handler_class = HandlerClass(handler_class)

        if handler_class.func_name_arg and not args and not kwargs.get(handler_class.func_name_arg):
            kwargs[handler_class.func_name_arg] = handler_func.__name__

        @wraps(handler_func)
        @handler_class.custom_wrapper
        def wrapper(update, context):
            self._logger.info(f"Request handled by '{handler_func.__name__}' ({update.effective_chat.id})")
            return handler_func(update, context)

        kwargs['callback'] = wrapper

        handler = handler_class.value(*args, **kwargs)
        self._dispatcher.add_handler(handler, group=group)

        if add_first:
            self._dispatcher.handlers[group].insert(0, self._dispatcher.handlers[group].pop())

    def add_first(self, *args, **kwargs):
        return self.add(add_first=True, *args, **kwargs)
