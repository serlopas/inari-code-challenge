from unittest import mock

import pytest

from app.core.error.game_exceptions import GameNotFoundError
from app.mastermind.game.data.services.game_query_service_impl import GameQueryServiceImpl
from app.mastermind.game.domain.entities.game_query_model import GameReadModel
from app.mastermind.game.domain.use_cases.retrieve_game_use_case import RetrieveGameUseCaseImpl
from tests.factories.game_factory import GamesFactory


class TestRetrieveGameUseCaseImpl:
    def test_call(self, session):
        service = GameQueryServiceImpl(session)
        game = GamesFactory()
        use_case = RetrieveGameUseCaseImpl(service)

        game_read_model = use_case((game.id,))

        assert isinstance(game_read_model, GameReadModel)
        assert game.id == game_read_model.id
        assert game.code == game_read_model.code
        assert game.status == game_read_model.status
        assert game.tries == game_read_model.tries
        assert game.max_tries == game_read_model.max_tries
        assert game_read_model.guesses == []
        assert game.created_at == game_read_model.created_at

    def test_call_game_not_found(self, faker, session):
        service = GameQueryServiceImpl(session)
        use_case = RetrieveGameUseCaseImpl(service)

        with pytest.raises(GameNotFoundError):
            use_case((faker.uuid4(),))

    def test_call_raises_exception(self, faker, session):
        service = GameQueryServiceImpl(session)
        use_case = RetrieveGameUseCaseImpl(service)

        with mock.patch.object(service, "find_by_id") as find_by_id_mock, pytest.raises(Exception):
            find_by_id_mock.side_effect = Exception
            use_case((faker.uuid4(),))
