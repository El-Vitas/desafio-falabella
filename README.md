# Pokémon Explorer

A web app that lists the first 100 Pokémon and statistics about their captures. The data is downloaded from the [Pokémon API](https://pokeapi.co), extended with the provided generator, and loaded into PostgreSQL by an Apache Airflow pipeline.

## Requirements

- Docker with Docker Compose

## How to run

```bash
cp .env.example .env
docker compose up
```

`.env` holds the local passwords; Compose stops if one is missing.

| Service | Address |
|---|---|
| Airflow | http://localhost:8080 (no login, local development only) |

SQL console: `docker compose exec postgres psql -U postgres -d pokemon`. Reset the database: `docker compose down -v`.

## Data extraction and generation

The `data-init` service runs on `docker compose up`, before Airflow, and writes six CSV files into `./data`:

1. `extraction/` downloads the first 100 Pokémon from PokeAPI into `pokemon.csv`, `types.csv` and `pokemon_types.csv`.
2. `generator/generate_pokemon_data.py` (unmodified) writes `trainers.csv`, `captures.csv` and `battles.csv`.

Airflow starts only if `data-init` succeeds, and reads `./data` read-only.

**Errors:** timeouts, `429` and `5xx` are retried up to 4 times with exponential backoff; `404` and invalid bodies fail at once. Nothing is written until the 100 Pokémon are validated; each file is written to a temporary file and renamed, and `data/_SUCCESS` is written last.

**Running it again:** if `data/_SUCCESS` exists the download is skipped; `FORCE_EXTRACT=true docker compose up data-init` downloads again. If PokeAPI is down, place the three CSV files and an empty `_SUCCESS` in `data/` by hand.

**File owner:** `data-init` runs as root to be able to write into `./data` on any host, then gives the files to the owner of the folder so they are not left owned by root on Linux.

## Tests

Only Docker is needed; the tests use a fake PokeAPI:

```bash
docker run --rm -v "$PWD":/repo:ro -w /repo -e PYTHONDONTWRITEBYTECODE=1 python:3.12.16-slim \
  sh -c "pip install -q -r extraction/requirements-dev.txt && python -m pytest -p no:cacheprovider extraction/tests"
```

## Repository layout

```
├── extraction/     downloads PokeAPI data into three CSV files
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
