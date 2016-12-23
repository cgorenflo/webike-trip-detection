class Event(object):
    def __init__(self, sender):
        self._handlers = set()
        self._sender = sender

    def handle(self, handler):
        self._handlers.add(handler)
        return self

    def unhandle(self, handler):
        try:
            self._handlers.remove(handler)
        except:
            raise ValueError("Handler is not handling this event, so cannot unhandle it.")
        return self

    def fire(self, *args, **kargs):
        for handler in self._handlers:
            handler(self._sender, *args, **kargs)

    def get_handler_count(self):
        return len(self._handlers)

    __iadd__ = handle
    __isub__ = unhandle
    __call__ = fire
    __len__ = get_handler_count

    def clear_handlers(self):
        self._handlers = set()
