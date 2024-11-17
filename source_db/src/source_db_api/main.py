from fastapi import FastAPI
from datetime import datetime, timedelta

from source_db_api.services import IntervalDataQueryService
from source_db_api.repository import SourceDbRepository


app = FastAPI()

@app.get("/get_data_interval")
async def get_data_interval(
    start_interval: datetime = datetime.now(),
    end_interval: datetime = datetime.now() + timedelta(minutes=10),
    fields: str = "timestamp,wind_speed,power,ambient_temperature"
    ):

    fields_to_retrive = fields.split(",")
    
    if start_interval > end_interval:
        return {"message": "Invalid interval"}
    
    allowed_fields = ["timestamp", "wind_speed", "power", "ambient_temperature"]
    fields_is_allowed = set(fields_to_retrive).issubset(set(allowed_fields))
    if not fields_is_allowed:
        return {"message": "Invalid fields"}

    service = IntervalDataQueryService(SourceDbRepository())
    return service.get_interval_data(start_interval, end_interval, fields_to_retrive)
