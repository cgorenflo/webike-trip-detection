import abc

from iss4e.webike.trips.sample import Sample


class Output(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def collect(self, start_sample, end_sample):
        pass


class InfluxOutput(Output):
    def __init__(self):
        self.points = []

    def collect(self, start_sample: Sample, end_sample: Sample):
        self.points.append(self._create_point(start_sample, {"start": True}))
        self.points.append(self._create_point(end_sample, {"end": True}))

    def _create_point(self, sample: Sample, fields):
        return {"measurement": "trips",
                "tags": {"imei": sample.imei},
                "time": sample["time"],
                "fields": fields
                }
