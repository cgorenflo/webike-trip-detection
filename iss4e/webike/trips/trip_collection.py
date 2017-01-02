from iss4e.webike.trips.sample import Sample
from iss4e.webike.trips.trip import Trip


class TripCollection(object):
    def __init__(self):
        self.finalized_trips = []
        self.current_trip = None
        self._start_trip()

    def process(self, sample:Sample):
        self.current_trip.process(sample)

    def _start_trip(self):
        trip = Trip()
        trip.finalized += self._handle_trip_finalized
        self.current_trip = trip

    def _handle_trip_finalized(self, sender, *args, **kargs):
        if kargs["is_valid"]:
            self.finalized_trips.append(sender)
        self._start_trip()
