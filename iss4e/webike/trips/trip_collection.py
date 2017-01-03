import logging
from typing import Iterable

from iss4e.webike.trips.sample import Sample
from iss4e.webike.trips.trip import Trip
from iss4e.util.brace_message import BraceMessage as __


class TripCollection(object):
    def __init__(self):
        self.trips = []
        self.logger = logging.getLogger("iss4e.webike.trips")
        self.current_trip = None
        self._start_trip()

    @property
    def finalized_trips(self) -> Iterable[Trip]:
        self.logger.debug(__("Return {count} trips", count=len(self.trips)))
        return self.trips

    def process(self, sample: Sample):
        self.current_trip.process(sample)

    def _start_trip(self):
        trip = Trip()
        trip.finalized += self._handle_trip_finalized
        self.current_trip = trip

    def _handle_trip_finalized(self, sender, *args, **kargs):
        self.logger.debug("Trip detected")
        if kargs["is_valid"]:
            self.trips.append(sender)
        self._start_trip()
