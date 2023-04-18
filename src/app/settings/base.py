from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    VERSION: str = "0.0.0"  # It MUST match the version in pyproject.toml file
    ENVIRONMENT: str
    DEBUG: Optional[bool] = False

    # Sentry - https://docs.sentry.io/platforms/python/guides/fastapi/
    USE_SENTRY: bool = False
    SENTRY_DSN: Optional[str] = None
    SENTRY_RELEASE: Optional[str] = None
    SENTRY_ENVIRONMENT: Optional[str] = None
    SENTRY_TRACES_SAMPLE_RATE: Optional[float] = 1.0

    DB_POSTGRES_DBNAME: str
    DB_POSTGRES_USER: str
    DB_POSTGRES_PASSWORD: str
    DB_POSTGRES_HOST: str
    DB_POSTGRES_PORT: int

    API_KEY: str

    MAX_TRIES: int = 10
    CODE_SIZE: int = 4

    class Config:
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
