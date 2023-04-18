from __future__ import annotations

from datetime import datetime

from pydantic import Field, BaseModel

from app.core.enums.enums import GameStatusEnum
from app.mastermind.game.domain.entities.game_entity import GameEntity
from app.mastermind.game.domain.entities.guess_query_model import GuessReadModel


class GameReadModel(BaseModel):
    id: str = Field(example="f7d690b539b048c99eaffe47cfe497a0")
    code: str = Field(example="RGGB")
    status: GameStatusEnum = Field(example="won")
    tries: int = Field(example=0)
    max_tries: int = Field(example=10)
    guesses: list[GuessReadModel]
    created_at: datetime

    class Config:
        orm_mode = True

    @staticmethod
    def from_entity(entity: GameEntity) -> GameReadModel:
        return GameReadModel(
            id=entity.id,
            code=entity.code,
            status=entity.status,
            tries=entity.tries,
            max_tries=entity.max_tries,
            created_at=entity.created_at,
            guesses=[GuessReadModel.from_entity(guess) for guess in entity.guesses] if entity.guesses else [],
        )
