from datetime import timedelta

from iss4e.webike.trips.event import Event
from iss4e.webike.trips.sample import Sample


class Trip:
    def __init__(self):
        self.is_finalized = False
        self.finalized = Event()
        self.discarded = Event()

        self._period = TripPeriod()

    def add(self, sample: Sample):
        if self.is_finalized:
            return

        if self._belongs_to_trip(sample):
            self._period.add(sample)
        elif self._trip_is_over(sample):
            self._validate_trip()

    def _belongs_to_trip(self, sample: Sample):
        return sample["discharge_current"] is not None and sample["discharge_current"] > 510

    def _trip_is_over(self, sample) -> bool:
        return self._period.end["time"] is not None and sample["time"] is not None and \
               sample["time"] - self._period.end["time"] >= timedelta(minutes=5)

    def _validate_trip(self):
        self.is_finalized = True
        if self._period.validate():
            self.finalized(self._period.start.sample, self._period.end.sample)
        else:
            self.discarded()


class TripPeriod(object):
    def __init__(self):
        self.start = Sample.empty()
        self.end = Sample.empty()

    def add(self, sample: Sample):
        if self.start == Sample.empty():
            self.start = sample
        else:
            self.end = sample

    def validate(self):
        return self.start.sample["time"] is not None and self.end.sample["time"] is not None and \
               self.end.sample["time"] - self.start.sample["time"] < timedelta(minutes=3)
