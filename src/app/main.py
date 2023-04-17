from fastapi import FastAPI

from app.core.database.postgres.database import engine
from app.core.models.postgres import models
from app.settings.base import get_settings
from app.third_parties import metrics
from app.third_parties.sentry import init_sentry_service
from app.logging.middleware import LoggingMiddleware

if get_settings().USE_SENTRY:
    init_sentry_service()

app = FastAPI(
    title="inari-code-challenge",
    version=get_settings().VERSION,
    debug=get_settings().DEBUG,
)

app.middleware("http")(LoggingMiddleware())

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
    models.BaseModel.metadata.create_all(bind=engine)
