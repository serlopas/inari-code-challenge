from sqlalchemy.orm import Session

from app.core.repositories.base_repository import BaseRepository
from app.mastermind.game.domain.entities.game_entity import GameEntity


class GameRepository(BaseRepository[GameEntity]):
    session: Session = NotImplementedError
