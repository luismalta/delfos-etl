from dataclasses import dataclass
from datetime import datetime
from psycopg2 import sql
from typing import Optional

from source_db_api.db_connection import PostgresPool

@dataclass
class IntervalDataDTO:
    timestamp: Optional[datetime] = None
    wind_speed: Optional[float] = None
    power: Optional[float] = None
    ambient_temperature: Optional[float] = None

    def to_dict(self):
        return {
            key: value for key, value in {
                "timestamp": self.timestamp,
                "wind_speed": self.wind_speed,
                "power": self.power,
                "ambient_temperature": self.ambient_temperature
            }.items() if value is not None
        }


class SourceDbRepositoryInterface:
    def get_data_by_interval(self) -> list[IntervalDataDTO]:
        raise NotImplementedError


class SourceDbRepository:
    def __init__(self):
        self.db_pool = PostgresPool()
    
    def _to_dto(self, rows, fields) -> list[dict]:
        return [IntervalDataDTO(**dict(zip(fields, row))).to_dict() for row in rows]


    def get_data_by_interval(self, start_interval: datetime, end_interval: datetime, fields: list[str]) -> list[IntervalDataDTO]:
        with self.db_pool.db_cursor() as cur:
            query = sql.SQL("SELECT {} FROM data WHERE timestamp BETWEEN %s AND %s").format(sql.SQL(', ').join([sql.Identifier(field) for field in fields]))
            cur.execute(query, (start_interval, end_interval))
            rows = cur.fetchall()
            return self._to_dto(rows, fields)