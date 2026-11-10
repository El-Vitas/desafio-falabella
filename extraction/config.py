import os
from pathlib import Path

from extraction.constants.settings import DATA_DIR_VARIABLE, FORCE_EXTRACT_VARIABLE, TRUTHY_ENV_VALUES
from extraction.errors import MissingSettingError
from extraction.models import Settings


def _required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise MissingSettingError(name)
    return value


def _flag(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in TRUTHY_ENV_VALUES


def load_settings() -> Settings:
    return Settings(
        data_dir=Path(_required(DATA_DIR_VARIABLE)),
        force_extract=_flag(FORCE_EXTRACT_VARIABLE),
    )
