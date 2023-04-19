from abc import abstractmethod
from typing import Optional

from sqlalchemy.orm import Session

from app.core.repositories.base_repository import BaseRepository
from app.mastermind.game.domain.entities.guess_entity import GuessEntity


class GuessRepository(BaseRepository[GuessEntity]):
    session: Session = NotImplementedError

    @abstractmethod
    def find_by_game_id(self, game_id: int) -> Optional[GuessEntity]:
        raise NotImplementedError()
