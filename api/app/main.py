from fastapi import FastAPI

from app import health

app = FastAPI(title="Pokémon Explorer API")
app.include_router(health.router)
