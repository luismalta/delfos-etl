from dagster import DailyPartitionsDefinition

from etl.assets.constants import START_DATE

daily_partition = DailyPartitionsDefinition(
    start_date=START_DATE,
)