from datetime import timedelta
from typing import List

from iss4e.webike.trips.event import Event
from iss4e.webike.trips.sample import Sample


class Trip:
    def __init__(self):
        self.finalized = Event(self)

        self._trip_samples = []
        self._trip_sample_candidates = []

        self._process = self._process_before_start_found

    @property
    def samples(self) -> List[Sample]:
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

    def process(self, sample: Sample):
        self._process(sample)

        if self._belongs_to_trip(sample):
            self._trip_samples += self._trip_sample_candidates
            self._trip_samples.append(sample)
        else:
            self._trip_sample_candidates.append(sample)

        if self._is_over():
            if self._validate():
                self.finalized(is_valid=True)
            else:
                self.finalized(is_valid=False)

    def _process_before_start_found(self, sample: Sample):
        if self._belongs_to_trip(sample):
            self._process = self._process_after_start_found
            self._trip_samples.append(sample)

    def _process_after_start_found(self, sample: Sample):
        if self._belongs_to_trip(sample):
            self._trip_samples += self._trip_sample_candidates
            self._trip_sample_candidates.clear()
            self._trip_samples.append(sample)
        else:
            self._trip_sample_candidates.append(sample)

            if self._is_over():
                self._process = lambda sample: None
                self.finalized(is_valid=self._validate())

    def _validate(self):
        return self._last_trip_sample["time"] is not None and self._first_trip_sample["time"] is not None and \
               self._last_trip_sample["time"] - self._first_trip_sample["time"] >= timedelta(minutes=3)

    def _is_over(self):
        return self._last_recorded_sample["time"] is not None and self._last_trip_sample["time"] is not None and \
               self._last_recorded_sample["time"] - self._last_trip_sample["time"] >= timedelta(minutes=5)

    def _belongs_to_trip(self, sample:Sample):
        return sample["discharge_current"] is not None and sample["discharge_current"] > 510
