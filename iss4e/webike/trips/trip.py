from datetime import timedelta
from typing import List

from iss4e.webike.trips.event import Event
from iss4e.webike.trips.sample import Sample


class Trip:
    def __init__(self, new_sample_received: Event):
        self.detected = Event(self)
        self.discarded = Event(self)

        self._trip_samples = []
        self._trip_sample_candidates = []

        new_sample_received += self._handle_new_sample_received
        self._unsubscribe_from_receiving_samples = lambda: self._unsubscrive_from(new_sample_received,
                                                                                  self._handle_new_sample_received)

    def _unsubscrive_from(self, event, handler):
        event -= handler

    @property
    def content(self) -> List[Sample]:
        return self._trip_samples

    @property
    def _first_trip_sample(self):
        return self._trip_samples[0] if self._trip_samples else Sample.empty()

    @property
    def _last_trip_sample(self):
        return self._trip_samples[-1] if self._trip_samples else Sample.empty()

    @property
    def _last_recorded_sample(self):
        return self._trip_sample_candidates[-1] if self._trip_sample_candidates else Sample.empty()

    def _handle_new_sample_received(self, sender, *args, **kargs):
        if not args and not kargs:
            return

        if "sample" in kargs.keys():
            sample = kargs["sample"]
        else:
            sample = args[0]

        self._process(sample)

    def _process(self, sample: Sample):
        if self._belongs_to_trip(sample):
            self._trip_samples += self._trip_sample_candidates
            self._trip_samples.append(sample)
        else:
            self._trip_sample_candidates.append(sample)

        if self._is_over():
            self._unsubscribe_from_receiving_samples()
            self._validate_trip()

    def _validate_trip(self):
        if self._validate():
            self.detected()
        else:
            self.discarded()

    def _validate(self):
        return self._last_trip_sample["time"] is not None and self._first_trip_sample["time"] is not None and \
               self._last_trip_sample["time"] - self._first_trip_sample["time"] >= timedelta(minutes=3)

    def _is_over(self):
        return self._last_recorded_sample["time"] is not None and self._last_trip_sample["time"] is not None and \
               self._last_recorded_sample["time"] - self._last_trip_sample["time"] >= timedelta(minutes=5)

    def _belongs_to_trip(self, sample):
        return sample["discharge_current"] is not None and sample["discharge_current"] > 510
