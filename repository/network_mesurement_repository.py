from influxdb_client import InfluxDBClient
from influxdb_client.client.flux_table import FluxRecord

from entity.network_measurement_entity import NetworkMeasurement


class NetworkMeasurementRepository:
    def __init__(self, client: InfluxDBClient, bucket: str):
        self.client = client
        self.bucket = bucket

    def get_last_readings(self, limit: int = 1000) -> list[NetworkMeasurement]:
        query = f'''
          from(bucket: "{self.bucket}")
            |> filter(fn: (r) => r._measurement == "network")
            |> limit(n:{limit})
          '''
        results = self.client.query_api().query(query)

        return self._map_records(results)

    # TODO: Adjust data mapping
    @classmethod
    def _map_records(cls, tables) -> list[NetworkMeasurement]:
        readings = []
        for table in tables:
            for record in table.records:
                readings.append(
                    NetworkMeasurement(
                        time=record.get_time(),
                        value=record.get_field("package_ratio")
                    )
                )
        return readings
