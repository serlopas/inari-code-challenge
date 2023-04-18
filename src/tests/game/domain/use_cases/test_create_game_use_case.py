from unittest import mock

import pytest

from app.mastermind.game.data.models.models import Game
from app.mastermind.game.data.repositories.game_repository_impl import GameRepositoryImpl
from app.mastermind.game.data.unit_of_works.game_unit_of_work_impl import GameUnitOfWorkImpl
from app.mastermind.game.domain.entities.game_query_model import GameReadModel
from app.mastermind.game.domain.use_cases.create_game_use_case import CreateGameUseCaseImpl


class TestCreateGameUseCaseImpl:
    def test_call(self, session):
        game_repository = GameRepositoryImpl(session)
        unit_of_work = GameUnitOfWorkImpl(game_repository)

        use_case = CreateGameUseCaseImpl(unit_of_work)

        game_read_model = use_case(None)
        assert isinstance(game_read_model, GameReadModel)

        game = session.get(Game, game_read_model.id)
        assert game is not None

        assert game.id == game_read_model.id
        assert game.code == game_read_model.code
        assert game.status == game_read_model.status
        assert game.tries == game_read_model.tries
        assert game.max_tries == game_read_model.max_tries
        assert game_read_model.guesses == []
        assert game.created_at == game_read_model.created_at

    def test_call_with_exception(self, session):
        game_repository = GameRepositoryImpl(session)
        unit_of_work = GameUnitOfWorkImpl(game_repository)
        use_case = CreateGameUseCaseImpl(unit_of_work)

        with mock.patch.object(game_repository, "create") as create_mock, mock.patch.object(
            unit_of_work, "rollback"
        ) as rollback_mock, pytest.raises(Exception):
            create_mock.side_effect = Exception
            use_case(None)

        create_mock.assert_called_once()
        rollback_mock.assert_called_once()
