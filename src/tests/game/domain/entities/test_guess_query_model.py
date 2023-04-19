import random

from app.core.enums.enums import GameStatusEnum
from app.mastermind.game.domain.entities.guess_query_model import GuessReadModel, GuessGameStatusReadModel


class TestGuessReadModel:
    def test_from_entity(self, guess_entity):
        guess_read_model = GuessReadModel.from_entity(guess_entity)

        assert isinstance(guess_read_model, GuessReadModel)
        assert guess_entity.id == guess_read_model.id
        assert guess_entity.guess_code == guess_read_model.guess_code
        assert guess_entity.white_pegs == guess_read_model.white_pegs
        assert guess_entity.black_pegs == guess_read_model.black_pegs
        assert guess_entity.game_id == guess_read_model.game_id
        assert guess_entity.created_at == guess_read_model.created_at


class TestGuessGameStatusReadModel:
    def test_from_entity(self, guess_entity):
        game_status = random.choice(list(GameStatusEnum))

        guess_game_status_read_model = GuessGameStatusReadModel.from_entity(guess_entity, game_status)

        assert isinstance(guess_game_status_read_model, GuessGameStatusReadModel)
        assert guess_entity.id == guess_game_status_read_model.id
        assert guess_entity.guess_code == guess_game_status_read_model.guess_code
        assert guess_entity.white_pegs == guess_game_status_read_model.white_pegs
        assert guess_entity.black_pegs == guess_game_status_read_model.black_pegs
        assert guess_entity.game_id == guess_game_status_read_model.game_id
        assert guess_entity.created_at == guess_game_status_read_model.created_at
        assert guess_game_status_read_model.game_status == game_status
