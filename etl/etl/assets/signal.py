import pandas as pd
from dagster import Output, asset

from etl.partitions import daily_partition
from etl.resources import SourceDBConnector, PostgresResource


@asset(partitions_def=daily_partition, group_name="signal")
def daily_signals_raw(
    context,
    source_db_connector: SourceDBConnector,
    postgres: PostgresResource):

    date = context.partition_key

    start_interval = date
    start_interval = pd.to_datetime(date).replace(hour=0, minute=0, second=0)
    end_interval = pd.to_datetime(date).replace(hour=23, minute=59, second=59)

    fields = "timestamp,wind_speed,power,ambient_temperature"

    data = source_db_connector.get_data_interval(start_interval, end_interval, fields)

    data_df = pd.DataFrame(data)

    postgres.save_dataframe("raw_source_data", data_df)


@asset(deps=["daily_signals_raw"], partitions_def=daily_partition, group_name="signal")
def daily_signals_10_mim_aggregated(
    context,
    postgres: PostgresResource):

    date = context.partition_key

    query = f"""
    SELECT
        timestamp,
        wind_speed,
        power,
        ambient_temperature
    FROM raw_source_data
    WHERE date(timestamp) = '{date}'
    """

    data = postgres.execute_query(query)

    data_df = pd.DataFrame(data)

    # Aggregate the data by 10 minutes intervals and calculate mean, min, max and std
    data_df.set_index('timestamp', inplace=True)
    aggregated_df = data_df.resample('10min').agg({
        'wind_speed': ['mean', 'min', 'max', 'std'],
        'power': ['mean', 'min', 'max', 'std']
    }).reset_index()

    # Flatten the MultiIndex columns
    aggregated_df.columns = ['_'.join(col).strip() if col[1] else col[0] for col in aggregated_df.columns.values]

    # Ensure that all signals exist in the signals table
    aggregated_df_columns = aggregated_df.columns.tolist()
    aggregated_df_columns.remove('timestamp')

    signals_query = """
        SELECT
            id,
            name
        FROM signal
    """
    data = list(postgres.execute_query(signals_query))

    for signal in aggregated_df_columns:
        if signal not in [row[1] for row in data]:
            postgres.execute_query(f"INSERT INTO signal (name) VALUES ('{signal}')")
    
    # Extract the signal ids
    data = list(postgres.execute_query(signals_query))
    signal_ids = {row[1]: row[0] for row in data}
            

    # Prepare the data for insertion
    frames = []
    for signal in aggregated_df_columns:
        signal_df = aggregated_df[['timestamp', signal]].copy()
        signal_df.rename(columns={signal: 'value'}, inplace=True)
        signal_df['signal_id'] = signal_ids[signal]
        frames.append(signal_df)

    postgres.save_dataframe("data", pd.concat(frames))

