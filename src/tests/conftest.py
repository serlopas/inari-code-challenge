import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.settings.base import get_settings


@pytest.fixture(autouse=True)
def restore_settings_after_test():
    settings = {**get_settings().dict()}
    yield
    for setting in settings.keys():
        setattr(get_settings(), setting, settings[setting])


@pytest.fixture(scope="function")
def app() -> FastAPI:
    from app.main import app  # local import for testing purpose

    return app


@pytest.fixture(scope="function")
def client(app) -> TestClient:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def authorized_client(client) -> TestClient:
    client.headers = {"X-API-Key": get_settings().API_KEY}
    return client
