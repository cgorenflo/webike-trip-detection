from iss4e.webike.trips import *


class TripDetector(object):
    def __init__(self):
        self.sample_received = Event()

        self._trips = set()
        self._start_trip()

    def processSamples(self, samples):
        for sample in samples:
            self.sample_received(sample)

        finalized_trips = []
        ongoing_trips = []

        for trip in self._trips:
            if trip.is_finalized:
                finalized_trips.append(trip)
            else:
                ongoing_trips.append(trip)

        self._trips = ongoing_trips
        return finalized_trips

    def _start_trip(self):
        self.sample_received.clear_handlers()
        trip = Trip()
        self.sample_received += trip.process
        trip.finalized += self._start_trip
        self._trips.add(trip)
