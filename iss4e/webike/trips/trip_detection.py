import logging
from datetime import timedelta
from typing import Iterable, List

from iss4e.webike.trips.auxiliary import Sample, Event
from iss4e.util.brace_message import BraceMessage as __


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
    def _last_recorded_candidate(self):
        return self._trip_sample_candidates[-1] if self._trip_sample_candidates else Sample.empty()

    def process(self, sample: Sample):
        self._process(sample)

    def _process_before_start_found(self, sample: Sample):
        if self._belongs_to_trip(sample):
            self._process = self._process_after_start_found
            self._trip_samples.append(sample)

    def _process_after_start_found(self, sample: Sample):
        self._trip_sample_candidates.append(sample)
        if self._is_over():
            self._process = lambda s: None
            self.finalized(is_valid=self._validate())

        elif self._belongs_to_trip(sample):
            self._trip_samples += self._trip_sample_candidates
            self._trip_sample_candidates.clear()

    def _belongs_to_trip(self, sample: Sample):
        return sample["discharge_current"] is not None and sample["discharge_current"] > 515

    def _is_over(self):
        return self._last_recorded_candidate["time"] is not None and self._last_trip_sample["time"] is not None and \
               self._last_recorded_candidate["time"] - self._last_trip_sample["time"] >= timedelta(minutes=5)

    def _validate(self):
        return self._last_trip_sample["time"] is not None and self._first_trip_sample["time"] is not None and \
               self._last_trip_sample["time"] - self._first_trip_sample["time"] >= timedelta(minutes=3)

    def snapshot(self):
        return {"samples": [sample.snapshot() for sample in self._trip_samples],
                "candidates": [sample.snapshot() for sample in self._trip_sample_candidates],
                "state": self._process.__name__}

    def restore(self, snapshot):
        self._trip_samples = [Sample.empty().restore(sample) for sample in snapshot["samples"]]
        self._trip_sample_candidates = [Sample.empty().restore(sample) for sample in snapshot["candidates"]]
        self._process = getattr(self, snapshot["state"])

        return self


class TripCollection(object):
    def __init__(self):
        self._trips = []
        self._logger = logging.getLogger("iss4e.webike.trips")
        self._current_trip = None
        self._current_sample = None
        self._start_trip()

    def read_finalized_trip_buffer(self) -> Iterable[Trip]:
        self._logger.debug(__("Return {count} trips", count=len(self._trips)))
        trips = self._trips
        self._trips = []
        return trips

    def process(self, sample: Sample):
        self._current_sample = sample
        self._current_trip.process(sample)

    def _start_trip(self):
        trip = Trip()
        trip.finalized += self._handle_trip_finalized
        self._current_trip = trip

    def _handle_trip_finalized(self, sender, is_valid: bool):
        if is_valid:
            self._trips.append(sender)
        self._start_trip()
        self._current_trip.process(self._current_sample)

    def snapshot(self):
        return {"trips": [trip.snapshot() for trip in self._trips], "current_trip": self._current_trip.snapshot()}

    def restore(self, snapshot: dict):
        for trip_snapshot in snapshot["trips"]:
            self._trips.append(Trip().restore(trip_snapshot))

        self._current_trip = Trip().restore(snapshot["current_trip"])

        return self
