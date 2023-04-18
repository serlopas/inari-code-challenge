from app.mastermind.game.domain.entities.guess_query_model import GuessReadModel


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
