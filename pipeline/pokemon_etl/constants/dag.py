from datetime import datetime

POKEMON_CONNECTION_ID = "pokemon_db"
DAG_START_DATE = datetime(2025, 1, 1)
LOAD_LOCK_TIMEOUT = "10s"
TASK_RETRIES = 2
TASK_RETRY_DELAY_SECONDS = 30
