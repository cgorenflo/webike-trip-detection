import string
from typing import Iterable

from iss4e.webike.trips.sample import Sample
from iss4e.webike.trips.trip import Trip



class InfluxPoints(object):
    def __init__(self, trips: Iterable[Trip]):
        self.points = []
        for trip in trips:
            if not trip.samples:
                continue

            self.points.append(self._create_point(trip.samples[0], {"start": True}))
            self.points.append(self._create_point(trip.samples[-1], {"end": True}))

    def _create_point(self, sample: Sample, fields):
        return {"measurement": "trips",
                "tags": {"imei": sample.imei},
                "time": sample["time"],
                "fields": fields
                }


class MySqlInsertQuery(object):
    def __init__(self, trips: Iterable[Trip]):
        self._values = [{"imei": trip.samples[0].imei, "start": trip.samples[0]["time"], "end": trip.samples[-1]["time"]} for trip in trips if trip.samples]

    def __str__(self):
        if not self._values:
            return ""

        return "INSERT INTO {table} {columns} VALUES {values};".format(table="trips", columns="(IMEI,start,end)",
                                                                       values=self._format_values())

    def _format_values(self) -> string:
        return ",".join("('{imei}','{start}','{end}')".format(**value) for value in self._values)
