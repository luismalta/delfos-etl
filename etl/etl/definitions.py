from dagster import Definitions, load_assets_from_modules

from etl.assets import signal  # noqa: TID252
from etl.jobs import daily_signals_job
from etl.schedules import daily_signals_schedule
from etl.resources import RESOURCES_PROD


all_assets = load_assets_from_modules([signal])
all_jobs = [daily_signals_job]
all_schedules = [daily_signals_schedule]

defs = Definitions(
    assets=all_assets,
    jobs=all_jobs,
    schedules=all_schedules,
    resources=RESOURCES_PROD,
)

