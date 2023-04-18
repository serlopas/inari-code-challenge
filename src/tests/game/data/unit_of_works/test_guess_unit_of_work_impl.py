from unittest import mock

from app.mastermind.game.data.repositories.guess_repository_impl import GuessRepositoryImpl
from app.mastermind.game.data.unit_of_works.guess_unit_of_work_impl import GuessUnitOfWorkImpl


class TestGuessUnitOfWorkImpl:
    def test_begin(self, session):
        guess_repository = GuessRepositoryImpl(session)
        unit_of_work = GuessUnitOfWorkImpl(guess_repository)

        with mock.patch.object(guess_repository.session, "begin") as begin_mock:
            unit_of_work.begin()

        begin_mock.assert_called_once()

    def test_commit(self, session):
        guess_repository = GuessRepositoryImpl(session)
        unit_of_work = GuessUnitOfWorkImpl(guess_repository)

        with mock.patch.object(guess_repository.session, "commit") as commit_mock:
            unit_of_work.commit()

        commit_mock.assert_called_once()

    def test_rollback(self, session):
        guess_repository = GuessRepositoryImpl(session)
        unit_of_work = GuessUnitOfWorkImpl(guess_repository)

        with mock.patch.object(guess_repository.session, "rollback") as rollback_mock:
            unit_of_work.rollback()

        rollback_mock.assert_called_once()
