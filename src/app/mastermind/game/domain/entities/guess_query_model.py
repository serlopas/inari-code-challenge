from __future__ import annotations

from datetime import datetime

from pydantic import Field, BaseModel

from app.core.enums.enums import GameStatusEnum
from app.mastermind.game.domain.entities.guess_entity import GuessEntity


class GuessReadModel(BaseModel):
    id: str = Field(example="f7d690b539b048c99eaffe47cfe497a0")
    guess_code: str = Field(example="rggb")
    white_pegs: int = Field(example="1")
    black_pegs: int = Field(example=1)
    game_id: str = Field(example="f7d690b539b048c99eaffe47cfe497a1")
    created_at: datetime

    class Config:
        orm_mode = True

    @staticmethod
    def from_entity(entity: GuessEntity) -> GuessReadModel:
        return GuessReadModel(
            id=entity.id,
            guess_code=entity.guess_code,
            white_pegs=entity.white_pegs,
            black_pegs=entity.black_pegs,
            game_id=entity.game_id,
            created_at=entity.created_at,
        )


class GuessGameStatusReadModel(BaseModel):
    id: str = Field(example="f7d690b539b048c99eaffe47cfe497a0")
    guess_code: str = Field(example="rbgb")
    white_pegs: int = Field(example="1")
    black_pegs: int = Field(example=1)
    game_id: str = Field(example="f7d690b539b048c99eaffe47cfe497a1")
    created_at: datetime
    game_status: str = Field(example=GameStatusEnum.in_progress)

    class Config:
        orm_mode = True

    @staticmethod
    def from_entity(entity: GuessEntity, game_status: str) -> GuessGameStatusReadModel:
        return GuessGameStatusReadModel(
            id=entity.id,
            guess_code=entity.guess_code,
            white_pegs=entity.white_pegs,
            black_pegs=entity.black_pegs,
            game_id=entity.game_id,
            created_at=entity.created_at,
            game_status=game_status,
        )
