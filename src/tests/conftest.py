import contextlib
import random
from contextvars import ContextVar
from datetime import datetime

import pytest
import sqlalchemy
from fastapi import FastAPI
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from starlette.testclient import TestClient

from app.core.database.postgres.database import get_session
from app.core.enums.enums import ColorsEnum, GameStatusEnum
from app.core.models.postgres.models import Base
from app.mastermind.game.domain.entities.game_entity import GameEntity
from app.mastermind.game.domain.entities.guess_entity import GuessEntity
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


session_for_factory = ContextVar("session_for_factory", default=None)


@pytest.fixture(scope="function")
def engine():
    settings = get_settings()
    postgres_database = "postgres"
    testing_database = f"testing_{settings.DB_POSTGRES_DBNAME}"
    db_url = (
        f"postgresql://{settings.DB_POSTGRES_USER}:{settings.DB_POSTGRES_PASSWORD}@{settings.DB_POSTGRES_HOST}:"
        f"{settings.DB_POSTGRES_PORT}/"
    )

    with sqlalchemy.create_engine(
        f"{db_url}{postgres_database}", isolation_level="AUTOCOMMIT"
    ).connect() as connection, contextlib.suppress(sqlalchemy.exc.ProgrammingError):
        connection.execute(text(f"CREATE DATABASE {testing_database}"))

    engine = create_engine(f"{db_url}{testing_database}")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield engine


@pytest.fixture(scope="function")
def session_maker(engine):
    yield sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session(engine, session_maker):
    from app.main import app  # local import for testing purpose

    connection = engine.connect()

    # begin a non-ORM transaction
    trans = connection.begin()

    db_session = session_maker()

    # start the session in a SAVEPOINT...
    db_session.begin_nested()

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_session] = override_get_db

    # then each time that SAVEPOINT ends, reopen it
    @event.listens_for(db_session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            # ensure that state is expired the way
            # session.commit() at the top level normally does
            # (optional step)
            session.expire_all()

            session.begin_nested()

    token = session_for_factory.set(db_session)
    yield db_session
    trans.rollback()
    db_session.close()
    session_for_factory.reset(token)


@pytest.fixture(scope="function")
def game_entity(faker) -> GameEntity:
    return GameEntity(
        id=faker.uuid4(),
        code="".join(random.choices(list(ColorsEnum), k=get_settings().CODE_SIZE)),
        status=random.choice(list(GameStatusEnum)),
        tries=faker.pyint(),
        max_tries=faker.pyint(),
        guesses=[],
        created_at=datetime.now(),
    )


@pytest.fixture(scope="function")
def guess_entity(faker) -> GuessEntity:
    return GuessEntity(
        id=faker.uuid4(),
        guess_code="".join(random.choices(list(ColorsEnum), k=get_settings().CODE_SIZE)),
        white_pegs=faker.pyint(),
        black_pegs=faker.pyint(),
        game_id=faker.uuid4(),
        created_at=datetime.now(),
    )


@pytest.fixture(scope="function")
def guess_code():
    return "".join(random.choices(list(ColorsEnum), k=get_settings().CODE_SIZE))
