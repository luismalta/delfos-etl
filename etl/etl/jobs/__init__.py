from dagster import define_asset_job, AssetSelection

from etl.partitions import daily_partition

daily_signals_job = define_asset_job(
    name="daily_signals_job",
    selection=AssetSelection.groups("signal"),
    partitions_def=daily_partition,
)