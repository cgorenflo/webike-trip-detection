from iss4e.db import influxdb
from iss4e.util.config import load_config

from iss4e.webike.trips import module_locator
from iss4e.webike.trips.output import InfluxPoints
from iss4e.webike.trips.sample import Sample
from iss4e.webike.trips.sample_stream import SampleStream

config = load_config(module_locator.module_path())
with influxdb.connect(**config["webike.influx"]) as client:
    measurement = client.stream_measurement(measurement="sensor_data",
                                            fields=["time", "discharge_current", "linear_acceleration_x",
                                                    "linear_acceleration_y", "linear_acceleration_z"])

    for _, series, samples in measurement:
        stream = SampleStream(Sample(series, sample) for sample in samples)
        output = InfluxPoints(stream.trip_detected)

        stream.process()
        client.write_points(output.points)
