import string
from typing import Iterable

import logging

from iss4e.webike.trips import Sample, Trip


def create_influx_points(trips: Iterable[Trip]) -> Iterable[dict]:
    points = []
    for trip in trips:
        if not trip.samples:
            continue

        points.append(_create_point(trip.samples[0], {"start": True}))
        points.append(_create_point(trip.samples[-1], {"end": True}))

    return points


def _create_point(sample: Sample, fields):
    return {"measurement": "trips",
            "tags": {"imei": sample.imei},
            "time": sample["time"],
            "fields": fields
            }


def create_mysql_query(trips: Iterable[Trip]):
    values = [{"imei": trip.samples[0].imei, "start": trip.samples[0]["time"], "end": trip.samples[-1]["time"]} for trip
              in trips if trip.samples]

    if not values:
        logger = logging.getLogger("iss4e.webike.trips")
        logger.debug("Empty query")
        return ""

    return "INSERT INTO {table} {columns} VALUES {values};".format(table="trips", columns="(IMEI,start,end)",
                                                                   values=_format_values(values))


def _format_values(values: Iterable[dict]) -> string:
    return ",".join("('{imei}','{start}','{end}')".format(**value) for value in values)
