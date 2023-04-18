from app.mastermind.game.domain.entities.guess_entity import GuessEntity


class TestGuessEntity:
    def test_eq(self, faker, guess_entity):
        # Check same id
        other_guess_entity = GuessEntity(**guess_entity.__dict__)
        assert guess_entity == other_guess_entity

        # Check different id
        other_guess_entity.id = faker.uuid4()
        assert guess_entity != other_guess_entity

        # Check with a non GuessEntity object
        assert guess_entity != guess_entity.__dict__
