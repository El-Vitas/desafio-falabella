import os
from dataclasses import dataclass, field

from app.shared.constants.settings import (
    CORS_ALLOWED_ORIGINS_VARIABLE,
    DATABASE_URL_VARIABLE,
    LIST_SEPARATOR,
)
from app.shared.errors import MissingSettingError


@dataclass(frozen=True)
class Settings:
    database_url: str = field(repr=False)
    cors_allowed_origins: tuple[str, ...]


def _required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise MissingSettingError(name)
    return value


def _required_list(name: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in _required(name).split(LIST_SEPARATOR) if item.strip())


def load_settings() -> Settings:
    return Settings(
        database_url=_required(DATABASE_URL_VARIABLE),
        cors_allowed_origins=_required_list(CORS_ALLOWED_ORIGINS_VARIABLE),
    )
