import os
import psycopg2
import psycopg2.pool
from contextlib import contextmanager

HOST = os.getenv('POSTGRES_HOST', 'localhost')
PORT = os.getenv('POSTGRES_PORT', '5432')
DATABASE = os.getenv('POSTGRES_DATABASE', 'source_db')
USER = os.getenv('POSTGRES_USER', 'source_db_user')
PASSWORD = os.getenv('POSTGRES_PASSWORD', 'source_db_password')


class PostgresPool:
    """
    PostgresPool is a class that manages a pool of connections to a PostgreSQL database using psycopg2's ThreadedConnectionPool.

    Attributes:
        dbpool (psycopg2.pool.ThreadedConnectionPool): A connection pool for managing PostgreSQL database connections.

    Methods:
        __init__():
            Initializes the PostgresPool instance by creating a ThreadedConnectionPool with the specified database connection parameters.

        db_cursor():
            A context manager that provides a database cursor for executing SQL queries. It establishes a connection to the database using the `dbpool` connection pool, and yields a cursor object for executing SQL queries. The connection is automatically committed if the execution of the queries is successful, or rolled back if an exception occurs. Finally, the connection is returned to the connection pool.
    """


    def __init__(self):
        self.dbpool = psycopg2.pool.ThreadedConnectionPool(
            host=HOST,
            port=PORT,
            dbname=DATABASE,
            user=USER,
            password=PASSWORD,
            minconn=1,
            maxconn=10
        )

    @contextmanager
    def db_cursor(self):
        """
        Provides a database cursor from the connection pool.

        This method yields a cursor object to interact with the database.
        It ensures that the connection is properly committed if the operations
        are successful, or rolled back in case of an exception. Finally, it
        returns the connection back to the pool.

        Yields:
            psycopg2.extensions.cursor: A cursor object to execute database operations.

        Raises:
            Exception: Any exception that occurs during the database operations.
        """
        conn = self.dbpool.getconn()
        try:
            with conn.cursor() as cur:
                yield cur
                conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            self.dbpool.putconn(conn)
