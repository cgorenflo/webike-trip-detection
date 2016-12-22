from datetime import datetime


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
