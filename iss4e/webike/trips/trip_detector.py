from typing import Iterable

from iss4e.webike.trips.sample import Sample
from iss4e.webike.trips.output import Output
from iss4e.webike.trips.trip import Trip


class TripDetector(object):
    def __init__(self, trip_output: Output):
        self._trip_output = trip_output
        self._trip = None
        self._start_trip()

    def process_samples(self, samples: Iterable[Sample]):
        for sample in samples:
            self._trip.add(sample)

    def _start_trip(self):
        self._trip = Trip()
        # suppress arguments for the start of a new trip
        self._trip.finalized += lambda start_sample, end_sample: self._start_trip()
        self._trip.finalized += self._trip_output.collect

        self._trip.discarded += self._start_trip
