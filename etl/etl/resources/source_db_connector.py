from dagster import ConfigurableResource
import httpx


class SourceDBConnector(ConfigurableResource):
    base_url: str
    port: int

    def get_data_interval(self, start_interval, end_interval, fields):
        params = {
            "start_interval": start_interval,
            "end_interval": end_interval,
            "fields": fields
        }

        data_interval_url = f"http://{self.base_url}:{self.port}/get_data_interval"

        data = httpx.get(data_interval_url, params=params)

        return data.json()
