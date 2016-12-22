from itertools import zip_longest

from iss4e.webike.trips.date_time import DateTime
from iss4e.webike.trips.imei import IMEI


class Sample(object):
    def __init__(self, series_selector: str, sample: dict):
        self._sample = sample
        if "time" in sample.keys():
            sample["time"] = DateTime(sample["time"])
        self.imei = IMEI(series_selector)

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
