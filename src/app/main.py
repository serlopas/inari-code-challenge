from fastapi import FastAPI

from app.core.database.postgres.database import engine
from app.core.models.postgres.models import Base
from app.logging.middleware import LoggingMiddleware
from app.mastermind.game.presentation.routes import create_game_route
from app.mastermind.game.presentation.routes import retrieve_game_route
from app.settings.base import get_settings
from app.third_parties import metrics
from app.third_parties.sentry import init_sentry_service

if get_settings().USE_SENTRY:
    init_sentry_service()

app = FastAPI(
    title="inari-code-challenge",
    version=get_settings().VERSION,
    debug=get_settings().DEBUG,
)

app.middleware("http")(LoggingMiddleware())

app.include_router(create_game_route.router, prefix="/games", tags=["games"])
app.include_router(retrieve_game_route.router, prefix="/games", tags=["retrive_games"])

prometheus_instrumentator = metrics.create_prometheus_instrumentator(app)


@app.get("/ping")
async def healthcheck():
    """
    Health check
    """
    return {"message": "pong"}


@app.on_event("startup")
async def startup():
    await metrics.expose_metric_service(app, prometheus_instrumentator)
    Base.metadata.create_all(bind=engine)
