from unittest import mock

import pytest

from app.mastermind.game.domain.entities.game_query_model import GameReadModel
from app.mastermind.game.repository.sqlalchemy.models.models import Game


class TestCreateGameUseCaseImpl:
    def test_call(self, create_game_use_case, session):
        game_read_model = create_game_use_case(None)
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

    def test_call_with_exception(self, create_game_use_case, session):
        with mock.patch.object(
            create_game_use_case.unit_of_work.repository, "create"
        ) as create_mock, mock.patch.object(
            create_game_use_case.unit_of_work, "rollback"
        ) as rollback_mock, pytest.raises(
            Exception
        ):
            create_mock.side_effect = Exception
            create_game_use_case(None)

        create_mock.assert_called_once()
        rollback_mock.assert_called_once()
