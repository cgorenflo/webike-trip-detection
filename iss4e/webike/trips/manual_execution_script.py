from concurrent.futures import ProcessPoolExecutor, wait
from itertools import chain
from iss4e.db import influxdb
from iss4e.util.config import load_config

from iss4e.webike.trips import module_locator, TripDetector, IMEI

def _execute(series, samples):
    trips = TripDetector(IMEI(series)).processSamples(samples)
    points = chain.from_iterable((trip.to_points() for trip in trips))
    client.write_points(points)


config = load_config(module_locator.module_path())
with influxdb.connect(**config["webike.influx"]) as client:
    measurement = client.stream_measurement(measurement="sensor_data",
                                            fields=["time", "discharge_current", "linear_acceleration_x",
                                                    "linear_acceleration_y", "linear_acceleration_z"])

    with ProcessPoolExecutor(max_workers=14) as executor:
        futures = [executor.submit(_execute, series, samples) for _, series, samples in measurement]

        wait(futures)
