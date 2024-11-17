#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "postgres" <<-EOSQL
	CREATE USER source_db_user WITH LOGIN PASSWORD 'source_db_password';
	CREATE DATABASE source_db;
	GRANT ALL PRIVILEGES ON DATABASE source_db TO source_db_user;
	ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO source_db_user;
    
EOSQL

psql -v ON_ERROR_STOP=1 --username "source_db_user" --dbname "source_db" <<-EOSQL
    CREATE TABLE "data" (
        timestamp TIMESTAMP PRIMARY KEY,
        wind_speed REAL,
        power REAL,
        ambient_temperature REAL
    );

EOSQL