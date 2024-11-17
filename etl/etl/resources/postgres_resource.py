import pandas as pd
from contextlib import contextmanager
from dagster import ConfigurableResource
from sqlalchemy import create_engine, URL, text
from sqlalchemy import exc


@contextmanager
def connect_postgres(config, schema="public"):
    url = URL.create(
        "postgresql+psycopg2",
        username=config["username"],
        password=config["password"],
        host=config["host"],
        port=config["port"],
        database=config["database"],
    )

    conn = None
    try:
        conn = create_engine(url).connect()
        yield conn
    finally:
        if conn:
            conn.commit()
            conn.close()


class PostgresResource(ConfigurableResource):
    username: str
    password: str
    host: str
    port: int
    database: str

    @property
    def _config(self):
        return self.dict()

    def execute_query(self, query):
        with connect_postgres(config=self._config) as engine:
            return engine.execute(text(query))

    def save_dataframe(self, table, dataframe):
        if isinstance(dataframe, pd.DataFrame):
            with connect_postgres(config=self._config) as engine:
                try:
                    dataframe.to_sql(table, engine, if_exists="append", index=False)
                except exc.IntegrityError:
                    print("Data already exists in the table")
        else:
            raise Exception("PostgresResource only supports pandas DataFrames")
