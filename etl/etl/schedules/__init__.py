from dagster import ScheduleDefinition
from etl.jobs import daily_signals_job

daily_signals_schedule = ScheduleDefinition(
    name="daily_signals_schedule",
    cron_schedule="0 0 * * *",
    job=daily_signals_job,
)