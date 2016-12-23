from typing import Iterable

from iss4e.webike.trips.event import Event
from iss4e.webike.trips.sample import Sample
from iss4e.webike.trips.trip import Trip


class SampleStream(object):
    def __init__(self, samples: Iterable[Sample]):
        self.new_sample_received = Event(self)
        self.trip_detected = Event(self)

        self._samples = samples
        self._start_trip()

    def process(self):
        for sample in self._samples:
            self.new_sample_received(sample)

    def _start_trip(self):
        trip = Trip(self.new_sample_received)
        trip.detected += self._handle_trip_detected
        trip.discarded += self._handle_trip_discarded

    def _handle_trip_detected(self, sender, *args, **kargs):
        self.trip_detected(sender)
        self._start_trip()

    def _handle_trip_discarded(self, sender, *args, **kargs):
        self._start_trip()
