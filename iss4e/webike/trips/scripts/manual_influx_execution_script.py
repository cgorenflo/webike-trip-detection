from iss4e.db import influxdb
from iss4e.util.config import load_config

import iss4e.webike.trips.output_variants as out
from iss4e.webike.trips import module_locator, Sample, TripCollection

config = load_config(module_locator.module_path())
with influxdb.connect(**config["webike.influx"]) as client:
    measurement = client.stream_measurement(measurement="sensor_data",
                                            fields=["time", "discharge_current", "linear_acceleration_x",
                                                    "linear_acceleration_y", "linear_acceleration_z"])

    for _, series, samples in measurement:
        trips = TripCollection()
        for sample in samples:
            trips.process(Sample(series, sample) )
        client.write_points(out.create_influx_points(trips.read_finalized_trip_buffer()))
