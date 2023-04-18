from app.mastermind.game.domain.entities.game_entity import GameEntity


class TestGameEntity:
    def test_eq(self, faker, game_entity):
        # Check same id
        other_game_entity = GameEntity(**game_entity.__dict__)
        assert game_entity == other_game_entity

        # Check different id
        other_game_entity.id = faker.uuid4()
        assert game_entity != other_game_entity

        # Check with a non GameEntity object
        assert game_entity != game_entity.__dict__
