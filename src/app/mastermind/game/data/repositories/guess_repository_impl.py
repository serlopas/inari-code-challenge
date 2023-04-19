from typing import Sequence, Optional

from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.mastermind.game.data.models.models import Guess
from app.mastermind.game.domain.entities.guess_entity import GuessEntity
from app.mastermind.game.domain.repositories.guess_repository import GuessRepository


class GuessRepositoryImpl(GuessRepository):
    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, entity: GuessEntity) -> GuessEntity:
        guess = Guess.from_entity(entity)

        self.session.add(guess)

        return guess.to_entity()

    def findall(self) -> Sequence[GuessEntity]:
        statement = select(Guess)

        try:
            result: Sequence[Guess] = self.session.execute(statement).scalars().all()
        except NoResultFound:
            return []

        return [guess.to_entity() for guess in result]

    def find_by_id(self, id: str) -> GuessEntity | None:
        result: Optional[Guess] = self.session.get(Guess, id)

        if result is None:
            return None

        return result.to_entity()

    def update(self, entity: GuessEntity) -> GuessEntity:
        guess = Guess.from_entity(entity)
        update_data = guess.to_dict()

        for key in [Guess.created_at.key, Guess.id.key]:
            update_data.pop(key),

        statement = update(Guess).where(Guess.id == guess.id).values(update_data).returning(Guess)

        result = self.session.execute(statement).scalar_one()

        return result.to_entity()

    def delete_by_id(self, id: str):
        statement = delete(Guess).filter_by(id=id)

        self.session.execute(statement)

    def find_by_game_id(self, game_id: int) -> Optional[GuessEntity]:
        statement = select(Guess).filter_by(game_id=game_id)

        try:
            result: Guess = self.session.execute(statement).scalar_one()
        except NoResultFound:
            return None

        return result.to_entity()
