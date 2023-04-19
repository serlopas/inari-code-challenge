from unittest import mock

from app.mastermind.game.repository.sqlalchemy.impl.game_repository_impl import SqlAlchemyGameRepositoryImpl
from app.mastermind.game.unit_of_work.impl.game_unit_of_work_impl import GameUnitOfWorkImpl


class TestGameUnitOfWorkImpl:
    def test_begin(self, session):
        game_repository = SqlAlchemyGameRepositoryImpl(session)
        unit_of_work = GameUnitOfWorkImpl(game_repository)

        with mock.patch.object(game_repository.session, "begin") as begin_mock:
            unit_of_work.begin()

        begin_mock.assert_called_once()

    def test_commit(self, session):
        game_repository = SqlAlchemyGameRepositoryImpl(session)
        unit_of_work = GameUnitOfWorkImpl(game_repository)

        with mock.patch.object(game_repository.session, "commit") as commit_mock:
            unit_of_work.commit()

        commit_mock.assert_called_once()

    def test_rollback(self, session):
        game_repository = SqlAlchemyGameRepositoryImpl(session)
        unit_of_work = GameUnitOfWorkImpl(game_repository)

        with mock.patch.object(game_repository.session, "rollback") as rollback_mock:
            unit_of_work.rollback()

        rollback_mock.assert_called_once()
