from app.mastermind.game.data.models.models import Game, Guess
from app.mastermind.game.domain.entities.game_entity import GameEntity
from app.mastermind.game.domain.entities.game_query_model import GameReadModel
from tests.factories.game_factory import GamesFactory
from tests.factories.guess_factory import GuessesFactory


class TestGame:
    def test_to_entity(self, session):
        game: Game = GamesFactory()

        game_entity = game.to_entity()

        assert isinstance(game_entity, GameEntity)
        assert game.id == game_entity.id
        assert game.code == game_entity.code
        assert game.status == game_entity.status
        assert game.tries == game_entity.tries
        assert game.max_tries == game_entity.max_tries
        assert game_entity.guesses == []
        assert game.created_at == game_entity.created_at

    def test_to_entity_with_guesses(self, session):
        game: Game = GuessesFactory().game

        game_entity = game.to_entity()

        assert isinstance(game_entity, GameEntity)
        assert game.id == game_entity.id
        assert game.code == game_entity.code
        assert game.status == game_entity.status
        assert game.tries == game_entity.tries
        assert game.max_tries == game_entity.max_tries
        assert game_entity.guesses == [guess.to_entity() for guess in game.guesses]
        assert game.created_at == game_entity.created_at

    def test_to_dict(self, session):
        game: Game = GamesFactory()
        expected_dict = {
            "id": game.id,
            "code": game.code,
            "status": game.status,
            "tries": game.tries,
            "max_tries": game.max_tries,
            "guesses": [],
            "created_at": game.created_at,
        }

        game_dict = game.to_dict()

        assert isinstance(game_dict, dict)
        assert game_dict == expected_dict

    def test_to_dict_with_guesses(self, session):
        game: Game = GuessesFactory().game
        expected_dict = {
            "id": game.id,
            "code": game.code,
            "status": game.status,
            "tries": game.tries,
            "max_tries": game.max_tries,
            "guesses": [guess.to_dict() for guess in game.guesses],
            "created_at": game.created_at,
        }

        game_dict = game.to_dict()

        assert isinstance(game_dict, dict)
        assert game_dict == expected_dict

    def test_to_read_model(self, session):
        game: Game = GamesFactory()

        game_read_model = game.to_read_model()

        assert isinstance(game_read_model, GameReadModel)
        assert game.id == game_read_model.id
        assert game.code == game_read_model.code
        assert game.status == game_read_model.status
        assert game.tries == game_read_model.tries
        assert game.max_tries == game_read_model.max_tries
        assert game_read_model.guesses == []
        assert game.created_at == game_read_model.created_at

    def test_to_read_model_with_guesses(self, session):
        game: Game = GuessesFactory().game

        game_read_model = game.to_read_model()

        assert isinstance(game_read_model, GameReadModel)
        assert game.id == game_read_model.id
        assert game.code == game_read_model.code
        assert game.status == game_read_model.status
        assert game.tries == game_read_model.tries
        assert game.max_tries == game_read_model.max_tries
        assert game_read_model.guesses == [guess.to_read_model() for guess in game.guesses]
        assert game.created_at == game_read_model.created_at

    def test_from_entity(self, game_entity, faker):
        game = Game.from_entity(game_entity)

        assert isinstance(game, Game)
        assert game.id == game_entity.id
        assert game.code == game_entity.code
        assert game.status == game_entity.status
        assert game.tries == game_entity.tries
        assert game.max_tries == game_entity.max_tries
        assert game.guesses == []
        assert game.created_at == game_entity.created_at

    def test_from_entity_with_guesses(self, game_entity, guess_entity, faker):
        game_entity.guesses = [guess_entity]

        game = Game.from_entity(game_entity)
        guess = [Guess.from_entity(guess) for guess in game_entity.guesses][0]

        assert isinstance(game, Game)
        assert game.id == game_entity.id
        assert game.code == game_entity.code
        assert game.status == game_entity.status
        assert game.tries == game_entity.tries
        assert game.max_tries == game_entity.max_tries
        assert game.created_at == game_entity.created_at
        assert guess.id == guess_entity.id
        assert guess.guess_code == guess_entity.guess_code
        assert guess.white_pegs == guess_entity.white_pegs
        assert guess.black_pegs == guess_entity.black_pegs
        assert guess.created_at == guess_entity.created_at
        assert guess.game_id == guess_entity.game_id
