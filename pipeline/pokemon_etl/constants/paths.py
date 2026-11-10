from pathlib import Path

DATA_DIR_VARIABLE = "POKEMON_DATA_DIR"
SUCCESS_MARKER_FILE_NAME = "_SUCCESS"

PACKAGE_DIR = Path(__file__).parent.parent
SCHEMA_SCRIPT = PACKAGE_DIR / "schema" / "schema.sql"
VIEWS_DIR = PACKAGE_DIR / "views"
