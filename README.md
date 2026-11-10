# Pokémon Explorer

A web app that lists the first 100 Pokémon and statistics about their captures. The data is downloaded from the [Pokémon API](https://pokeapi.co), extended with the provided generator, and loaded into PostgreSQL by an Apache Airflow pipeline.

## Requirements

- Docker with Docker Compose

## How to run

```bash
cp .env.example .env
docker compose up
```

The `.env` file holds the local database passwords. Compose stops with a clear message if a variable is missing.

| Service | Address |
|---|---|
| Airflow | http://localhost:8080 (no login: local development only) |

To open a SQL console on the Pokémon database:

```bash
docker compose exec postgres psql -U postgres -d pokemon
```

To start again from an empty database:

```bash
docker compose down -v
```

## Repository layout

```
├── generator/      the provided data generator, unmodified
├── database/init/  creates the databases and users, only when the data volume is empty
└── docker-compose.yml
```

## Database users

| User | Database | Can |
|---|---|---|
| `airflow` | `airflow` | Airflow's internal metadata |
| `pokemon_loader` | `pokemon` | Create tables and write: used by the DAG |
| `pokemon_api` | `pokemon` | Read only: used by the API |
