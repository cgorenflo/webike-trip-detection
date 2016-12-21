from iss4e.webike.trips import *
from iss4e.webike.trips.imei import IMEI


class Trip:
    def __init__(self, imei: IMEI):
        self._imei = imei

        self._trip_in_progress_rules = self._create_in_progress_rules()
        self._trip_ended_rules = self._create_ended_rules()

        self._start_value = None
        self._end_value = None
        self.is_finalized = False

        self.finalized = Event()
        self.end_changed = Event()

        self._process = self._pre_trip_start

    def process(self, sample):
        self._process(sample)

    def to_points(self):
        if not self.is_finalized:
            return ()

        return (
            self._create_point(self._start_value, {"start": True}), self._create_point(self._end_value, {"end": True}))

    def _pre_trip_start(self, sample):
        if self._belongs_to_trip(sample):
            self._start_value = sample
            self._process = self._trip_in_progress

    def _trip_in_progress(self, sample):
        if not self._belongs_to_trip(sample):
            self._set_end(sample)
            self._process = self._post_possible_trip_end

    def _post_possible_trip_end(self, sample):
        if self._trip_end_is_certain(sample):
            self._finalize()

        elif self._belongs_to_trip(sample):
            self._set_end(sample)

    def _set_end(self, sample):
        self._end_value = sample
        self.end_changed(self._end_value)

    def _finalize(self):
        self.is_finalized = True
        self.finalized()

    def _belongs_to_trip(self, sample):
        return [rule for rule in self._trip_in_progress_rules if rule.belongs_to_trip(sample)]

    def _trip_end_is_certain(self, sample):
        return [rule for rule in self._trip_ended_rules if not rule.belongs_to_trip(sample)]

    def _create_in_progress_rules(self):
        discharge_current_rule = Rule(lambda sample: sample["discharge_current"] > 510)
        return [discharge_current_rule]

    def _create_ended_rules(self):
        idle_rule = IdleRule(self.end_changed)
        return [idle_rule]

    def _create_point(self, time, fields: dict):
        return {"measurement": "trips",
                "tags": {"imei": self._imei},
                "time": time,
                "fields": fields
                }
