#!/usr/bin/env bash
set -euo pipefail

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres <<-SQL
    CREATE ROLE airflow LOGIN PASSWORD '${AIRFLOW_DB_PASSWORD}';
    CREATE DATABASE airflow OWNER airflow;

    CREATE ROLE pokemon_loader LOGIN PASSWORD '${POKEMON_LOADER_PASSWORD}';
    CREATE ROLE pokemon_api LOGIN PASSWORD '${POKEMON_API_PASSWORD}';
    CREATE DATABASE pokemon OWNER pokemon_loader;
SQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname pokemon <<-SQL
    REVOKE CREATE ON SCHEMA public FROM PUBLIC;
    GRANT USAGE, CREATE ON SCHEMA public TO pokemon_loader;
    GRANT USAGE ON SCHEMA public TO pokemon_api;
    ALTER DEFAULT PRIVILEGES FOR ROLE pokemon_loader IN SCHEMA public
        GRANT SELECT ON TABLES TO pokemon_api;
SQL
