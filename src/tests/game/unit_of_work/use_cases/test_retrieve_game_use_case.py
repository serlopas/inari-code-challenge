from unittest import mock

import pytest

from app.core.error.game_exceptions import GameNotFoundError
from app.mastermind.game.domain.entities.game_query_model import GameReadModel
from app.mastermind.game.unit_of_work.use_cases.retrieve_game_use_case import RetrieveGameUseArgs
from tests.factories.game_factory import GamesFactory


class TestRetrieveGameUseCaseImpl:
    def test_call(self, retrieve_game_use_case, session):
        game = GamesFactory()

        game_read_model = retrieve_game_use_case(RetrieveGameUseArgs(game_id=game.id))

        assert isinstance(game_read_model, GameReadModel)
        assert game.id == game_read_model.id
        assert game.code == game_read_model.code
        assert game.status == game_read_model.status
        assert game.tries == game_read_model.tries
        assert game.max_tries == game_read_model.max_tries
        assert game_read_model.guesses == []
        assert game.created_at == game_read_model.created_at

    def test_call_game_not_found(self, retrieve_game_use_case, faker, session):
        with pytest.raises(GameNotFoundError):
            retrieve_game_use_case(RetrieveGameUseArgs(game_id=faker.uuid4()))

    def test_call_raises_exception(self, retrieve_game_use_case, faker, session):
        with mock.patch.object(retrieve_game_use_case.service, "find_by_id") as find_by_id_mock, pytest.raises(
            Exception
        ):
            find_by_id_mock.side_effect = Exception
            retrieve_game_use_case(RetrieveGameUseArgs(game_id=faker.uuid4()))
