from app.mastermind.game.data.models.models import Guess
from app.mastermind.game.data.repositories.guess_repository_impl import GuessRepositoryImpl
from app.mastermind.game.domain.entities.guess_entity import GuessEntity
from tests.factories.game_factory import GamesFactory
from tests.factories.guess_factory import GuessesFactory


class TestGuessRepositoryImpl:
    def test_create(self, guess_entity, session):
        GamesFactory(id=guess_entity.game_id)
        guess_entity_returned = GuessRepositoryImpl(session).create(guess_entity)
        session.commit()

        result = session.get(Guess, guess_entity.id)

        assert result is not None
        assert isinstance(result, Guess)
        assert result.id == guess_entity_returned.id == guess_entity.id
        assert result.guess_code == guess_entity_returned.guess_code == guess_entity.guess_code
        assert result.white_pegs == guess_entity_returned.white_pegs == guess_entity.white_pegs
        assert result.black_pegs == guess_entity_returned.black_pegs == guess_entity.black_pegs
        assert result.game_id == guess_entity_returned.game_id == guess_entity.game_id
        assert result.created_at == guess_entity_returned.created_at == guess_entity.created_at

    def test_findall(self, session):
        guess: Guess = GuessesFactory()

        guess_entities_returned = GuessRepositoryImpl(session).findall()

        assert len(guess_entities_returned) == 1

        guess_entity = guess_entities_returned[0]

        assert isinstance(guess_entity, GuessEntity)
        assert guess.id == guess_entity.id
        assert guess.guess_code == guess_entity.guess_code
        assert guess.white_pegs == guess_entity.white_pegs
        assert guess.black_pegs == guess_entity.black_pegs
        assert guess.game_id == guess_entity.game_id
        assert guess.created_at == guess_entity.created_at

    def test_findall_but_table_empty(self, session):
        assert GuessRepositoryImpl(session).findall() == []

    def test_find_by_id(self, session):
        guess: Guess = GuessesFactory()

        guess_entity_returned = GuessRepositoryImpl(session).find_by_id(id=guess.id)

        assert isinstance(guess_entity_returned, GuessEntity)
        assert guess.id == guess_entity_returned.id
        assert guess.guess_code == guess_entity_returned.guess_code
        assert guess.white_pegs == guess_entity_returned.white_pegs
        assert guess.black_pegs == guess_entity_returned.black_pegs
        assert guess.game_id == guess_entity_returned.game_id
        assert guess.created_at == guess_entity_returned.created_at

    def test_find_by_id_element_not_found(self, faker, session):
        assert GuessRepositoryImpl(session).find_by_id(id=faker.uuid4()) is None

    def test_update(self, faker, session):
        guess: Guess = GuessesFactory()
        white_pegs = guess.white_pegs
        guess_entity = guess.to_entity()
        guess_entity.white_pegs = faker.pyint()

        assert guess.white_pegs == white_pegs

        guess_entity_returned = GuessRepositoryImpl(session).update(entity=guess_entity)
        guess_updated = session.get(Guess, guess_entity.id)

        assert isinstance(guess_entity_returned, GuessEntity)
        assert guess_entity_returned.white_pegs == guess_entity.white_pegs == guess_updated.white_pegs

    def test_delete_by_id(self, session):
        guess: Guess = GuessesFactory()

        GuessRepositoryImpl(session).delete_by_id(id=guess.id)
        result = session.get(Guess, guess.id)

        assert result is None

    def test_find_by_game_id(self, session):
        guess: Guess = GuessesFactory()

        guess_entity_returned = GuessRepositoryImpl(session).find_by_game_id(game_id=guess.game_id)

        assert isinstance(guess_entity_returned, GuessEntity)
        assert guess.id == guess_entity_returned.id
        assert guess.guess_code == guess_entity_returned.guess_code
        assert guess.white_pegs == guess_entity_returned.white_pegs
        assert guess.black_pegs == guess_entity_returned.black_pegs
        assert guess.game_id == guess_entity_returned.game_id
        assert guess.created_at == guess_entity_returned.created_at

    def test_find_by_game_id_element_not_found(self, faker, session):
        assert GuessRepositoryImpl(session).find_by_game_id(game_id=faker.uuid4()) is None
