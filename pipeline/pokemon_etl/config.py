import os
from pathlib import Path

from pokemon_etl.constants.paths import DATA_DIR_VARIABLE
from pokemon_etl.errors import MissingSettingError


def data_dir() -> Path:
    value = os.environ.get(DATA_DIR_VARIABLE, "").strip()
    if not value:
        raise MissingSettingError(DATA_DIR_VARIABLE)
    return Path(value)
