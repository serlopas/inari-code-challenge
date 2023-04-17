from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.settings.base import get_settings

__SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{get_settings().DB_POSTGRES_USER}:{get_settings().DB_POSTGRES_PASSWORD}@"
    f"{get_settings().DB_POSTGRES_HOST}:{get_settings().DB_POSTGRES_PORT}/"
    f"{get_settings().DB_POSTGRES_DBNAME}"
)

engine = create_engine(__SQLALCHEMY_DATABASE_URL, future=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_session() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
