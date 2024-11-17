from dagster import EnvVar
from etl.resources.source_db_connector import SourceDBConnector
from etl.resources.postgres_resource import PostgresResource

CONNECTOR_URL = EnvVar("CONNECTOR_URL").get_value("localhost")
CONNECTOR_PORT = EnvVar("CONNECTOR_PORT").get_value("8000")

POSTGRES_USER = EnvVar("POSTGRES_USER").get_value("postgres")
POSTGRES_PASSWORD = EnvVar("POSTGRES_PASSWORD").get_value("postgres")
POSTGRES_HOST = EnvVar("POSTGRES_HOST").get_value("localhost")
POSTGRES_PORT = EnvVar("POSTGRES_PORT").get_value("5432")
POSTGRES_DB = EnvVar("POSTGRES_DB").get_value("postgres")


RESOURCES_PROD = {
    'source_db_connector': SourceDBConnector(
        base_url=CONNECTOR_URL,
        port=CONNECTOR_PORT
    ),
    'postgres': PostgresResource(
        username=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
    ),
}
