from iss4e.db import influxdb
from iss4e.util.config import load_config

from iss4e.webike.trips import module_locator, Sample, TripCollection
import iss4e.webike.trips.scripts.output_variants as out

config = load_config(module_locator.module_path())
with influxdb.connect(**config["webike.influx"]) as client:
    measurement = client.stream_measurement(measurement="sensor_data",
                                            fields=["time", "discharge_current", "linear_acceleration_x",
                                                    "linear_acceleration_y", "linear_acceleration_z"])

    for _, series, samples in measurement:
        trips = TripCollection()
        for sample in samples:
            trips.process(Sample(series, sample) )
        client.write_points(out.create_influx_points(trips.finalized_trips))
