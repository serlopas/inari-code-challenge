from typing import Sequence, Optional

from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.mastermind.game.data.models.models import Game
from app.mastermind.game.domain.entities.game_entity import GameEntity
from app.mastermind.game.domain.repositories.game_repository import GameRepository


class GameRepositoryImpl(GameRepository):
    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, entity: GameEntity) -> GameEntity:
        game = Game.from_entity(entity)

        self.session.add(game)

        return game.to_entity()

    def findall(self) -> Sequence[GameEntity]:
        statement = select(Game)

        try:
            result: Sequence[Game] = self.session.execute(statement).scalars().all()
        except NoResultFound:
            return []

        return [game.to_entity() for game in result]

    def find_by_id(self, id: int) -> GameEntity | None:
        result: Optional[Game] = self.session.get(Game, id)

        if result is None:
            return None

        return result.to_entity()

    def update(self, entity: GameEntity) -> GameEntity:
        game = Game.from_entity(entity)
        update_data = game.to_dict()

        for key in [Game.created_at.key, Game.id.key, Game.guesses.key]:
            update_data.pop(key),

        statement = update(Game).where(Game.id == game.id).values(update_data).returning(Game)

        result = self.session.execute(statement).scalar_one()

        return result.to_entity()

    def delete_by_id(self, id: int):
        statement = delete(Game).filter_by(id=id)

        self.session.execute(statement)
