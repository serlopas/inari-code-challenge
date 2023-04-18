from app.mastermind.game.data.models.models import Guess
from app.mastermind.game.data.services.guess_query_service_impl import GuessQueryServiceImpl
from app.mastermind.game.domain.entities.guess_query_model import GuessReadModel
from tests.factories.guess_factory import GuessesFactory


class TestGuessQueryServiceImpl:
    def test_find_by_id(self, session):
        guess: Guess = GuessesFactory()

        guess_read_model_returned = GuessQueryServiceImpl(session).find_by_id(id=guess.id)

        assert isinstance(guess_read_model_returned, GuessReadModel)
        assert guess.id == guess_read_model_returned.id
        assert guess.guess_code == guess_read_model_returned.guess_code
        assert guess.white_pegs == guess_read_model_returned.white_pegs
        assert guess.black_pegs == guess_read_model_returned.black_pegs
        assert guess.game_id == guess_read_model_returned.game_id
        assert guess.created_at == guess_read_model_returned.created_at

    def test_find_by_id_element_not_found(self, faker, session):
        assert GuessQueryServiceImpl(session).find_by_id(id=faker.uuid4()) is None

    def test_findall(self, session):
        guess: Guess = GuessesFactory()

        guess_entities_returned = GuessQueryServiceImpl(session).findall()

        assert len(guess_entities_returned) == 1

        guess_read_model = guess_entities_returned[0]

        assert isinstance(guess_read_model, GuessReadModel)
        assert guess.id == guess_read_model.id
        assert guess.guess_code == guess_read_model.guess_code
        assert guess.white_pegs == guess_read_model.white_pegs
        assert guess.black_pegs == guess_read_model.black_pegs
        assert guess.game_id == guess_read_model.game_id
        assert guess.created_at == guess_read_model.created_at

    def test_findall_but_table_empty(self, session):
        assert GuessQueryServiceImpl(session).findall() == []
