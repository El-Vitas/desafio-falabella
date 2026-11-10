from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.shared.constants.openapi import UNUSED_VALIDATION_SCHEMAS, UNUSED_VALIDATION_STATUS


def _without_validation_responses(schema: dict[str, Any]) -> dict[str, Any]:
    for path_item in schema["paths"].values():
        for operation in path_item.values():
            operation["responses"].pop(UNUSED_VALIDATION_STATUS, None)
    component_schemas = schema.get("components", {}).get("schemas", {})
    for name in UNUSED_VALIDATION_SCHEMAS:
        component_schemas.pop(name, None)
    return schema


def openapi_schema(app: FastAPI) -> dict[str, Any]:
    if app.openapi_schema is None:
        app.openapi_schema = _without_validation_responses(
            get_openapi(title=app.title, version=app.version, routes=app.routes)
        )
    return app.openapi_schema
