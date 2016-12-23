from iss4e.webike.trips.event import Event
from iss4e.webike.trips.sample import Sample
from iss4e.webike.trips.trip import Trip


class InfluxPoints(object):
    def __init__(self, trip_detected: Event):
        self.points = []

        trip_detected += self._handle_trip_detected

    def _handle_trip_detected(self, trip):
        self._collect(trip)

    def _collect(self, trip: Trip):
        if not trip.content:
            return

        self.points.append(self._create_point(trip.content[0], {"start": True}))
        self.points.append(self._create_point(trip.content[-1], {"end": True}))

    def _create_point(self, sample: Sample, fields):
        return {"measurement": "trips",
                "tags": {"imei": sample.imei},
                "time": sample["time"],
                "fields": fields
                }


class MySqlInsertQuery(object):
    def __init__(self, trip_detected: Event):
        self._values = []
        trip_detected += self._handle_trip_detected

    def _handle_trip_detected(self, trip):
        self._collect(trip)

    def _collect(self, trip: Trip):
        if not trip.content:
            return
        self._values.append(
            {"imei": trip.content[0].imei, "start": trip.content[0]["time"], "end": trip.content[-1]["time"]})

    def to_string(self):
        return "INSERT INTO {table} {columns} VALUES {values}".format(table="trips", columns="(IMEI,start,end)",
                                                                      values=self._get_values())

    def _get_values(self):
        ",".join("({imei},{start},{end})".format(**value) for value in self._values)
