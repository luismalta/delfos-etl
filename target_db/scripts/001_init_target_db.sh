#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "postgres" <<-EOSQL
	CREATE USER dagster_user WITH LOGIN PASSWORD 'dagster_db_password';
	CREATE DATABASE dagster;
	GRANT ALL PRIVILEGES ON DATABASE dagster TO dagster_user;
	ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO dagster_user;
    
EOSQL

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "postgres" <<-EOSQL
	CREATE USER target_db_user WITH LOGIN PASSWORD 'target_db_password';
	CREATE DATABASE target_db;
	GRANT ALL PRIVILEGES ON DATABASE target_db TO target_db_user;
	ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO target_db_user;
    
EOSQL
