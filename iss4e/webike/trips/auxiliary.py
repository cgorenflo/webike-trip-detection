from datetime import datetime
from itertools import zip_longest


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


class DateTime(object):
    def __init__(self, time_string: str):
        self._time_string = time_string
        self._datetime = datetime.strptime(time_string.split(".")[0].split("Z")[0], '%Y-%m-%dT%H:%M:%S')

    def __sub__(self, other):
        return self._datetime - other

    def __rsub__(self, other):
        return other - self._datetime

    def __str__(self):
        return self._time_string


class IMEI(object):
    def __init__(self, series_selector: str):
        self._series_selector = "" if series_selector == "" else series_selector.split("'")[1]

    def __str__(self):
        return self._series_selector

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._series_selector == other._series_selector
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self == other
        return NotImplemented


class Sample(object):
    def __init__(self, series_selector: str, sample: dict):
        self.imei = IMEI(series_selector)

        self._sample = sample
        if "time" in sample.keys():
            sample["time"] = DateTime(sample["time"])

    def __getitem__(self, item):
        if item in self._sample.keys():
            return self._sample[item]
        else:
            return None

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            zipped = zip_longest(sorted(vars(self).items()), sorted(vars(other).items()))
            for (key1, value1), (key2, value2) in zipped:
                if key1 != key2:
                    return False
                elif value1 != value2:
                    return False

            return True
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self == other
        return NotImplemented

    @staticmethod
    def empty():
        return Sample("", {})
