import random
import uuid
from datetime import datetime

from app.core.enums.enums import ColorsEnum
from app.mastermind.game.domain.entities.guess_entity import GuessEntity
from app.mastermind.game.domain.entities.guess_query_model import GuessReadModel
from app.mastermind.game.repository.sqlalchemy.models.models import Guess
from app.settings.base import get_settings
from tests.factories.guess_factory import GuessesFactory


class TestGuess:
    def test_to_entity(self, session):
        guess: Guess = GuessesFactory()

        guess_entity = guess.to_entity()

        assert isinstance(guess_entity, GuessEntity)
        assert guess.id == guess_entity.id
        assert guess.guess_code == guess_entity.guess_code
        assert guess.white_pegs == guess_entity.white_pegs
        assert guess.black_pegs == guess_entity.black_pegs
        assert guess.game_id == guess_entity.game_id
        assert guess.created_at == guess_entity.created_at

    def test_to_dict(self, session):
        guess: Guess = GuessesFactory()
        expected_dict = {
            "id": guess.id,
            "guess_code": guess.guess_code,
            "white_pegs": guess.white_pegs,
            "black_pegs": guess.black_pegs,
            "game_id": guess.game_id,
            "created_at": guess.created_at,
        }

        guess_dict = guess.to_dict()

        assert isinstance(guess_dict, dict)
        assert guess_dict == expected_dict

    def test_to_read_model(self, session):
        guess: Guess = GuessesFactory()

        guess_read_model = guess.to_read_model()

        assert isinstance(guess_read_model, GuessReadModel)
        assert guess.id == guess_read_model.id
        assert guess.guess_code == guess_read_model.guess_code
        assert guess.white_pegs == guess_read_model.white_pegs
        assert guess.black_pegs == guess_read_model.black_pegs
        assert guess.game_id == guess_read_model.game_id
        assert guess.created_at == guess_read_model.created_at

    def test_from_entity(self, faker):
        guess_entity = GuessEntity(
            id=uuid.uuid4().hex,
            guess_code="".join(random.choices(list(ColorsEnum), k=get_settings().CODE_SIZE)),
            white_pegs=faker.pyint(),
            black_pegs=faker.pyint(),
            game_id=uuid.uuid4().hex,
            created_at=datetime.now(),
        )

        guess = Guess.from_entity(guess_entity)

        assert isinstance(guess, Guess)
        assert guess.id == guess_entity.id
        assert guess.guess_code == guess_entity.guess_code
        assert guess.white_pegs == guess_entity.white_pegs
        assert guess.black_pegs == guess_entity.black_pegs
        assert guess.game_id == guess_entity.game_id
        assert guess.created_at == guess_entity.created_at
