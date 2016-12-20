import abc

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
        self.FIVE_MINUTES = 5*60
        self.end_sample = None
        end_changed_event += self._update_end_sample

    def belongs_to_trip(self, sample):
        return self.end_sample is None or sample["time"] - self.end_sample["time"] <= self.FIVE_MINUTES

    def _update_end_sample(self, sample):
        self.end_sample = sample

