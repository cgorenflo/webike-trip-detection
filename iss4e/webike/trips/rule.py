import abc
from datetime import datetime, timedelta


class RuleBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def belongs_to_trip(self, sample):
        pass


class Rule(object):
    def __init__(self, testing_function):
        self.function = testing_function

    def belongs_to_trip(self, sample):
        return self.function(sample)


class IdleRule(RuleBase):
    def __init__(self, end_changed_event):
        self.FIVE_MINUTES = timedelta(minutes=5)
        self.end_sample = None
        end_changed_event += self._update_end_sample

    def belongs_to_trip(self, sample):
        return self.end_sample is None or self.to_datetime(sample["time"]) - self.to_datetime(
            self.end_sample["time"]) <= self.FIVE_MINUTES

    def to_datetime(self, time_string: str):
        return datetime.strptime(time_string.split(".")[0].split("Z")[0], '%Y-%m-%dT%H:%M:%S')

    def _update_end_sample(self, sample):
        self.end_sample = sample
