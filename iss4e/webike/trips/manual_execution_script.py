from iss4e.db import influxdb
from iss4e.util.config import load_config

from iss4e.webike.trips import module_locator
from iss4e.webike.trips.output import InfluxOutput
from iss4e.webike.trips.sample import Sample
from iss4e.webike.trips.trip_detector import TripDetector

config = load_config(module_locator.module_path())
with influxdb.connect(**config["webike.influx"]) as client:
    measurement = client.stream_measurement(measurement="sensor_data",
                                            fields=["time", "discharge_current", "linear_acceleration_x",
                                                    "linear_acceleration_y", "linear_acceleration_z"])

    for _, series, samples in measurement:
        output = InfluxOutput()
        TripDetector(output).process_samples(Sample(series, sample) for sample in samples)
        client.write_points(output.points)
