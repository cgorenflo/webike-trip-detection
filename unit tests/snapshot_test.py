import unittest

from iss4e.webike.trips import TripCollection, Sample


class SnapShotTest(unittest.TestCase):
    def setUp(self):
        self.samples = [Sample("123", {"time": '2015-01-01T11:00:00', "discharge_current": 500}),
                        Sample("123", {"time": '2015-01-01T11:00:01', "discharge_current": 540}),
                        Sample("123", {"time": '2015-01-01T11:02:02', "discharge_current": 560}),
                        Sample("123", {"time": '2015-01-01T11:04:03', "discharge_current": 580}),
                        Sample("123", {"time": '2015-01-01T11:04:04', "discharge_current": 501}),
                        Sample("123", {"time": '2015-01-01T11:15:00', "discharge_current": 500}),
                        Sample("123", {"time": '2015-01-01T11:31:00', "discharge_current": 800}),
                        Sample("123", {"time": '2015-01-01T11:31:01', "discharge_current": 900})]

        self.trips = TripCollection()
        for sample in self.samples:
            self.trips.process(sample)

    def test_restore_snapshot_finalized_trips_correct(self):
        snapshot = self.trips.snapshot()
        restored_trips = TripCollection().restore(snapshot)

        finalized_trips = self.trips.read_finalized_trip_buffer()
        restored_finalized_trips = restored_trips.read_finalized_trip_buffer()

        self.assertEqual(len(restored_finalized_trips), len(finalized_trips))
        for trip1, trip2 in zip(restored_finalized_trips,finalized_trips):
            self.assertListEqual(trip1.samples, trip2.samples)

    def test_restore_snapshot_open_trip_correct(self):
        snapshot = self.trips.snapshot()
        restored_trips = TripCollection().restore(snapshot)

        new_samples = [Sample("123", {"time": '2015-01-01T11:33:01', "discharge_current": 902}),
                       Sample("123", {"time": '2015-01-01T11:35:01', "discharge_current": 802}),
                       Sample("123", {"time": '2015-01-01T12:35:01', "discharge_current": 502})]

        for sample in new_samples:
            self.trips.process(sample)
            restored_trips.process(sample)

        finalized_trips = self.trips.read_finalized_trip_buffer()
        restored_finalized_trips = restored_trips.read_finalized_trip_buffer()

        self.assertEqual(len(restored_finalized_trips), len(finalized_trips))
        for trip1, trip2 in zip(restored_finalized_trips, finalized_trips):
            self.assertListEqual(trip1.samples, trip2.samples)

        if __name__ == '__main__':
            unittest.main()
