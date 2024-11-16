from datetime import datetime
from source_db_api.repository import SourceDbRepositoryInterface, IntervalDataDTO


class IntervalDataQueryService:
    def __init__(self, respository: SourceDbRepositoryInterface):
        self.respository = respository

    def get_interval_data(self, start_interval: datetime, end_interval: datetime, fields: list[str]) -> list[IntervalDataDTO]:
        return self.respository.get_data_by_interval(start_interval, end_interval, fields)
        