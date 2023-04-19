from app.mastermind.game.repository.sqlalchemy.models.models import Game
from app.mastermind.game.unit_of_work.impl.game_query_service_impl import GameQueryServiceImpl
from app.mastermind.game.domain.entities.game_query_model import GameReadModel
from tests.factories.game_factory import GamesFactory


class TestGameQueryServiceImpl:
    def test_find_by_id(self, session):
        game: Game = GamesFactory()

        game_read_model_returned = GameQueryServiceImpl(session).find_by_id(id=game.id)

        assert isinstance(game_read_model_returned, GameReadModel)
        assert game.id == game_read_model_returned.id
        assert game.code == game_read_model_returned.code
        assert game.status == game_read_model_returned.status
        assert game.tries == game_read_model_returned.tries
        assert game.max_tries == game_read_model_returned.max_tries
        assert game_read_model_returned.guesses == [guess.to_entity() for guess in game.guesses]
        assert game.created_at == game_read_model_returned.created_at

    def test_find_by_id_element_not_found(self, faker, session):
        assert GameQueryServiceImpl(session).find_by_id(id=faker.uuid4()) is None

    def test_findall(self, session):
        game: Game = GamesFactory()

        game_read_model_returned = GameQueryServiceImpl(session).findall()

        assert len(game_read_model_returned) == 1

        game_read_model = game_read_model_returned[0]

        assert isinstance(game_read_model, GameReadModel)
        assert game.id == game_read_model.id
        assert game.code == game_read_model.code
        assert game.status == game_read_model.status
        assert game.tries == game_read_model.tries
        assert game.max_tries == game_read_model.max_tries
        assert game_read_model.guesses == [guess.to_entity() for guess in game.guesses]
        assert game.created_at == game_read_model.created_at

    def test_findall_but_table_empty(self, session):
        assert GameQueryServiceImpl(session).findall() == []
