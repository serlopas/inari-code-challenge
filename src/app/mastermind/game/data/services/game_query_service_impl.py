from typing import Sequence, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.mastermind.game.data.models.models import Game
from app.mastermind.game.domain.entities.game_query_model import GameReadModel
from app.mastermind.game.domain.services.game_query_service import GameQueryService


class GameQueryServiceImpl(GameQueryService):
    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_id(self, id: str) -> Optional[GameReadModel]:
        result: Optional[Game] = self.session.get(Game, id)

        if result is None:
            return None

        return result.to_read_model()

    def findall(self) -> Sequence[GameReadModel]:
        statement = select(Game)

        result = self.session.execute(statement).scalars().all()

        return [game.to_read_model() for game in result]
