from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from starlette import status

from app.dependencies import api_key_validator
from app.settings.base import get_settings


class TestApiKeyValidator:
    @staticmethod
    def _generate_app_test() -> FastAPI:
        app_test = FastAPI()

        @app_test.get("/ping")
        async def auth_healthcheck(_: None = Depends(api_key_validator)):
            return {"message": "pong"}

        return app_test

    def test_api_key_auh(self):
        with TestClient(self._generate_app_test()) as client:
            # missing api key
            response = client.get("/ping")
            assert response.status_code == status.HTTP_403_FORBIDDEN

            # bad api key
            response = client.get("/ping", headers={"X-API-Key": "badapikey"})
            assert response.status_code == status.HTTP_403_FORBIDDEN

            # good api key
            response = client.get("/ping", headers={"X-API-Key": get_settings().API_KEY})
            assert response.status_code == status.HTTP_200_OK
