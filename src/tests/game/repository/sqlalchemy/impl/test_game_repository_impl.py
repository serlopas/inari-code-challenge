from app.mastermind.game.repository.sqlalchemy.models.models import Game
from app.mastermind.game.repository.sqlalchemy.impl.game_repository_impl import SqlAlchemyGameRepositoryImpl
from app.mastermind.game.domain.entities.game_entity import GameEntity
from tests.factories.game_factory import GamesFactory


class TestGameRepositoryImpl:
    def test_create(self, game_entity, session):
        game_entity_returned = SqlAlchemyGameRepositoryImpl(session).create(game_entity)
        session.commit()

        result = session.get(Game, game_entity.id)

        assert result is not None
        assert isinstance(result, Game)
        assert result.id == game_entity_returned.id == game_entity.id
        assert result.code == game_entity_returned.code == game_entity.code
        assert result.status == game_entity_returned.status == game_entity.status
        assert result.tries == game_entity_returned.tries == game_entity.tries
        assert result.max_tries == game_entity_returned.max_tries == game_entity.max_tries
        assert result.guesses == []
        assert result.created_at == game_entity_returned.created_at == game_entity.created_at

    def test_findall(self, session):
        game: Game = GamesFactory()

        game_entities_returned = SqlAlchemyGameRepositoryImpl(session).findall()

        assert len(game_entities_returned) == 1

        game_entity = game_entities_returned[0]

        assert isinstance(game_entity, GameEntity)
        assert game.id == game_entity.id
        assert game.code == game_entity.code
        assert game.status == game_entity.status
        assert game.tries == game_entity.tries
        assert game.max_tries == game_entity.max_tries
        assert game_entity.guesses == [guess.to_entity() for guess in game.guesses]
        assert game.created_at == game_entity.created_at

    def test_findall_but_table_empty(self, session):
        assert SqlAlchemyGameRepositoryImpl(session).findall() == []

    def test_find_by_id(self, session):
        game: Game = GamesFactory()

        game_entity_returned = SqlAlchemyGameRepositoryImpl(session).find_by_id(id=game.id)

        assert isinstance(game_entity_returned, GameEntity)
        assert game.id == game_entity_returned.id
        assert game.code == game_entity_returned.code
        assert game.status == game_entity_returned.status
        assert game.tries == game_entity_returned.tries
        assert game.max_tries == game_entity_returned.max_tries
        assert game_entity_returned.guesses == [guess.to_entity() for guess in game.guesses]
        assert game.created_at == game_entity_returned.created_at

    def test_find_by_id_element_not_found(self, faker, session):
        assert SqlAlchemyGameRepositoryImpl(session).find_by_id(id=faker.uuid4()) is None

    def test_update(self, session):
        game: Game = GamesFactory()
        game_entity = game.to_entity()
        game_entity.tries += 1

        assert game.tries == 0

        game_entity_returned = SqlAlchemyGameRepositoryImpl(session).update(entity=game_entity)
        game_updated = session.get(Game, game_entity.id)

        assert isinstance(game_entity_returned, GameEntity)
        assert game_entity_returned.tries == game_entity.tries == game_updated.tries

    def test_delete_by_id(self, session):
        game: Game = GamesFactory()

        SqlAlchemyGameRepositoryImpl(session).delete_by_id(id=game.id)
        result = session.get(Game, game.id)

        assert result is None
