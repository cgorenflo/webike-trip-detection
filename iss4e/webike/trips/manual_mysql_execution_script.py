from iss4e.db import mysql, influxdb
from iss4e.util.config import load_config
import logging

from iss4e.webike.trips import module_locator
from iss4e.webike.trips.output import MySqlInsertQuery
from iss4e.webike.trips.sample import Sample
from iss4e.webike.trips.sample_stream import SampleStream
from iss4e.util.brace_message import BraceMessage as __

config = load_config(module_locator.module_path())
logger = logging.getLogger("iss4e.webike.trips")

with influxdb.connect(**config["webike.influx"]) as influx_client, \
        mysql.connect(**config["webike.mysql"]) as my_sql_client:
    measurement = influx_client.stream_measurement(measurement="sensor_data",
                                                   fields=["time", "discharge_current", "linear_acceleration_x",
                                                           "linear_acceleration_y", "linear_acceleration_z"])

    for _, series, samples in measurement:
        stream = SampleStream(Sample(series, sample) for sample in samples)
        output = MySqlInsertQuery(stream.trip_detected)

        stream.process()
        try:
            my_sql_client.query(output.to_string())
        except:
            logger.error(__("Query that lead to the error:\n{query}", query=output.to_string()))
