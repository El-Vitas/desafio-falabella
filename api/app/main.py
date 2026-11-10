from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from functools import partial

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import health
from app.pokemon import router as pokemon
from app.shared.config import Settings, load_settings
from app.shared.constants.http import ALLOWED_METHODS
from app.shared.database import create_pool
from app.shared.error_handlers import register_error_handlers
from app.shared.openapi import openapi_schema
from app.stats import router as stats


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.pool = create_pool(app.state.settings.database_url)
    app.state.pool.open(wait=False)
    yield
    app.state.pool.close()


def build_app(settings: Settings) -> FastAPI:
    app = FastAPI(title="Pokémon Explorer API", lifespan=lifespan)
    app.state.settings = settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_allowed_origins),
        allow_methods=list(ALLOWED_METHODS),
    )
    register_error_handlers(app)
    app.include_router(health.router)
    app.include_router(pokemon.router)
    app.include_router(stats.router)
    app.openapi = partial(openapi_schema, app)
    return app


def create_app() -> FastAPI:
    return build_app(load_settings())
