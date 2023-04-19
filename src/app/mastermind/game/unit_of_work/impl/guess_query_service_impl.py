from typing import Sequence, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.mastermind.game.repository.sqlalchemy.models.models import Guess
from app.mastermind.game.domain.entities.guess_query_model import GuessReadModel
from app.mastermind.game.unit_of_work.base.guess_query_service import GuessQueryService


class GuessQueryServiceImpl(GuessQueryService):
    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_id(self, id: str) -> Optional[GuessReadModel]:
        result: Optional[Guess] = self.session.get(Guess, id)

        if result is None:
            return None

        return result.to_read_model()

    def findall(self) -> Sequence[GuessReadModel]:
        statement = select(Guess)

        result = self.session.execute(statement).scalars().all()

        return [guess.to_read_model() for guess in result]
