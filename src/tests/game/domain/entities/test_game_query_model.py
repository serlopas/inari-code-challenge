from app.mastermind.game.domain.entities.game_query_model import GameReadModel


class TestGameReadModel:
    def test_from_entity(self, game_entity):
        game_read_model = GameReadModel.from_entity(game_entity)

        assert isinstance(game_read_model, GameReadModel)
        assert game_entity.id == game_read_model.id
        assert game_entity.code == game_read_model.code
        assert game_entity.status == game_read_model.status
        assert game_entity.tries == game_read_model.tries
        assert game_entity.max_tries == game_read_model.max_tries
        assert game_entity.guesses == []
        assert game_entity.created_at == game_read_model.created_at
