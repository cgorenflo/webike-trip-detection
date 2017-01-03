import json

from iss4e.db import mysql
from iss4e.util.config import load_config
from kapacitor.udf.agent import Agent, Handler
from kapacitor.udf import udf_pb2

from iss4e.webike.trips import module_locator, TripCollection, Sample
from iss4e.webike.trips.output_variants import create_mysql_query


class TripHandler(Handler):
    def __init__(self):
        self._trips_by_imei = {}
        self._config = load_config(module_locator.module_path())

    def info(self):
        response = udf_pb2.Response()
        response.info.wants = udf_pb2.STREAM
        response.info.provides = udf_pb2.STREAM

        return response

    def init(self, init_req):
        success = True
        msg = ""

        response = udf_pb2.Response()
        response.init.success = success
        response.init.error = msg[1:]

        return response

    def snapshot(self):
        snapshot = {}
        for imei, trips in self._trips_by_imei.items():
            snapshot[imei] = trips.snapshot()

        response = udf_pb2.Response()
        response.snapshot.snapshot = json.dumps(snapshot)

        return response

    def restore(self, restore_req):
        msg = ''
        try:
            for imei, trips in json.loads(restore_req.snapshot):
                self._trips_by_imei[imei] = TripCollection().restore(trips)
            success = True
        except Exception as e:
            success = False
            msg = str(e)

        response = udf_pb2.Response()
        response.restore.success = success
        response.restore.error = msg

        return response

    def begin_batch(self, begin_req):
        raise Exception("not supported")

    def point(self, point):
        sample = Sample(point.tags["imei"], {"time": point.time,
                                             "discharge_current": point.fieldsInt["discharge_current"]})

        if str(sample.imei) not in self._trips_by_imei.keys():
            self._trips_by_imei[str(sample.imei)] = TripCollection()

        self._trips_by_imei[str(sample.imei)].process(sample)

        queries = []
        for trip_collection in self._trips_by_imei.values():
            trips = trip_collection.read_finalized_trip_buffer()
            query = create_mysql_query(trips)

            if query:
                queries.append(query)

        if queries:
            with mysql.connect(**self._config["webike.mysql"]) as client:
                for query in queries:
                    client.query(query)

    def end_batch(self, end_req):
        raise Exception("not supported")


if __name__ == '__main__':
    agent = Agent()
    handler = TripHandler()
    agent.handler = handler

    agent.start()
    agent.wait()
